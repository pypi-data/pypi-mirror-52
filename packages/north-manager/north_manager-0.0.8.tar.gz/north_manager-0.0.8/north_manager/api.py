from typing import Optional, Tuple, Sequence, List, NamedTuple
import re
import os
import time
import logging
from os import path
from functools import lru_cache
from xml.dom import minidom
from configparser import ConfigParser
from subprocess import call
from tempfile import NamedTemporaryFile
import requests
from ftdi_serial import Serial, SerialException

logger = logging.getLogger(__name__)


BASE_PATH = path.dirname(path.realpath(__file__))
BIN_PATH = path.join(BASE_PATH, 'bin', 'windows')
PROPELLENT_PATH = path.join(BIN_PATH, 'Propellent')

config = ConfigParser()
config.read(path.join(BASE_PATH, 'config.ini'))

AWS_BUCKET = config.get('DEFAULT', 'FIRMWARE_URL')
FIRMWARE_REGEX = '(\w+)-(\w+)-v(\d+)\.(\d+)\.(\d+)\.binary'
INFO_REGEX = 'North (\w+)-(\w+)-?(\w+)?, v?(\d+)\.(\d+)\.(\d+)'
VERSION_REGEX = 'v?(\d+)\.(\d+)\.(\d+)'

_get_xml_bucket_list_value = None

FirmwareVersion = Tuple[int, int, int]
FirmwareFilenameInfo = Sequence[str]


class NorthManagerError(Exception):
    pass


class NorthManagerFirmwareNotFoundError(NorthManagerError):
    pass


class FirmwareInfo(NamedTuple):
    controller: str = 'c9'
    model: str = 'n9'
    version: FirmwareVersion = (0, 0, 0)

    @classmethod
    def from_filename(cls, filename: str) -> Optional['FirmwareInfo']:
        try:
            controller, model, major, minor, patch = re.search(FIRMWARE_REGEX, filename).groups()
            return FirmwareInfo(controller.lower(), model.lower(), (int(major), int(minor), int(patch)))
        except AttributeError:
            return None

    @property
    def filename(self) -> str:
        return f'{self}.binary'

    def __str__(self):
        return f'{self.controller}-{self.model}-v{self.version[0]}.{self.version[1]}.{self.version[2]}'.lower()

    @property
    def name(self) -> str:
        return f'North {self.controller.upper()}-{self.model.upper()}, v{self.version[0]}.{self.version[1]}.{self.version[2]}'

    @property
    def up_to_date(self) -> bool:
        return self.version >= get_latest_firmware_version_for_model(self.model, self.controller)


class ControllerInfo(NamedTuple):
    port: Optional[str] = None
    variant: Optional[str] = None
    firmware: Optional[FirmwareInfo] = None

    @classmethod
    def from_info(cls, info, port=None) -> Optional['ControllerInfo']:
        try:
            controller, model, variant, major, minor, patch = re.search(INFO_REGEX, info).groups()
            return ControllerInfo(port, variant.lower(), FirmwareInfo(controller.lower(), model.lower(), (int(major), int(minor), int(patch))))
        except AttributeError:
            return None

    def __str__(self):
        variant_str = '-' + self.variant.upper() if self.variant is not None else ''
        return f'North {self.firmware.controller.upper()}-{self.firmware.model.upper()}{variant_str}, ' + \
               f'v{self.firmware.version[0]}.{self.firmware.version[1]}.{self.firmware.version[2]}'

    @property
    def unknown(self) -> bool:
        return self.firmware is None

    @property
    def name(self) -> str:
        if self.firmware is None:
            return 'Unknown'

        return self.firmware.name

    @property
    def item(self) -> str:
        return f'{self.port}: {self.name}'

    @property
    def up_to_date(self) -> bool:
        if self.firmware is None:
            return False

        return self.firmware.up_to_date


def parse_version(version: str) -> Optional[FirmwareVersion]:
    try:
        major, minor, patch = re.search(VERSION_REGEX, version).groups()
        return int(major), int(minor), int(patch)
    except AttributeError:
        return None


def download_firmware(firmware: FirmwareInfo) -> str:
    firmware_file = path.join(BASE_PATH, 'firmware', firmware.filename)

    if path.exists(firmware_file):
        os.remove(firmware_file)

    firmware_url = AWS_BUCKET + '/' + firmware.filename
    logger.info(f'Downloading firmware: {firmware_url}')
    response = requests.get(firmware_url)

    if not response.ok:
        raise NorthManagerFirmwareNotFoundError(f'Cannot find firmware: {firmware}')

    with open(firmware_file.lower(), 'wb') as f:
        f.write(response.content)

    return firmware_file


def request_controller_info(port, retries=3) -> ControllerInfo:
    if retries == 0:
        return ControllerInfo(port=port)

    serial = Serial(device_port=port)
    time.sleep(0.5)
    try:
        response = serial.request(b'info\r', line_ending=b'\r\n', timeout=0.2)
        serial.disconnect()

        return ControllerInfo.from_info(response.decode(), port)
    except Exception as err:
        time.sleep(0.5)
        return request_controller_info(port, retries-1)


def detect_controllers(include_unknown=False) -> List[ControllerInfo]:
    logger.info(f'Detecting connected controllers...')

    ports = sorted(Serial.list_device_ports(), key=lambda p: int(p.strip('COM')))
    controllers = []
    time.sleep(2)  # listing ports can reset connected C9s, wait for them to boot
    for port in ports:
        try:
            info = request_controller_info(port)
            if info is not None:
                controllers.append(info)
            elif include_unknown:
                controllers.append(ControllerInfo(port=port))
        except Exception:
            if include_unknown:
                controllers.append(ControllerInfo(port=port))

    return controllers


@lru_cache(maxsize=None)
def get_firmware_list()-> List[FirmwareInfo]:
    global _get_xml_bucket_list_value
    if _get_xml_bucket_list_value is not None:
        return _get_xml_bucket_list_value

    request = requests.get(AWS_BUCKET)
    xml = minidom.parseString(request.text)
    key_els = xml.getElementsByTagName('Key')
    files = [key.childNodes[0].nodeValue for key in key_els]
    _get_xml_bucket_list_value = files

    return [FirmwareInfo.from_filename(file) for file in files]


@lru_cache(maxsize=None)
def get_models() -> List[str]:
    return list(set([firmware.model for firmware in get_firmware_list()]))


@lru_cache(maxsize=None)
def get_controllers() -> List[str]:
    return list(set([firmware.controller for firmware in get_firmware_list()]))


@lru_cache(maxsize=None)
def get_firmware_list_for_model(model_name, controller_name='c9') -> List[FirmwareInfo]:
    return [firmware for firmware in get_firmware_list() if firmware.controller == controller_name.lower() and firmware.model == model_name.lower()]


@lru_cache(maxsize=None)
def get_firmware_versions_for_model(model_name, controller_name='c9'):
    versions = [firmware.version for firmware in get_firmware_list_for_model(model_name, controller_name)]
    return sorted(versions, reverse=True)


def get_latest_firmware_version_for_model(model_name, controller_name='c9'):
    try:
        return get_firmware_versions_for_model(model_name, controller_name)[0]
    except IndexError:
        return None


def flash_firmware(firmware_file, ram=False, port=None):
    logger.info(f'Flashing firmware: {firmware_file}')
    command = PROPELLENT_PATH

    if not ram:
        command += ' /eeprom'

    if port is not None:
        command += ' /port ' + port

    command += ' ' + path.realpath(firmware_file)
    call(command)


def download_and_flash_firmware(model_name, controller_name='c9', version=None, ram=False, port=None):
    version = get_latest_firmware_version_for_model(model_name, controller_name) if version is None else version
    firmware = FirmwareInfo(controller_name, model_name, version)
    firmware_file = download_firmware(firmware)
    flash_firmware(firmware_file, ram=ram, port=port)
    os.remove(firmware_file)
