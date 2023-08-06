from typing import List, Tuple
from PyQt5.QtCore import QTimer
from ftdi_serial import Serial
from north_manager.gui.object import Object, objectProperty, computedProperty
from north_manager import api
from north_manager.api import ControllerInfo


def find_index(items, item, default_index=0) -> int:
    try:
        return items.index(item)
    except ValueError:
        return default_index


class Messages:
    FINDING_DEVICES = 'Finding devices...'
    NO_DEVICES_FOUND = 'No devices found'
    UP_TO_DATE = ' is up to date'
    NEW_VERSION_AVAILABLE = ' has a new version available'


class Device(Object):
    controller: ControllerInfo = None


class State(Object):
    test: str
    enabled: bool = True
    devices: List[Device] = []
    devicesEnabled: bool = False
    devicesIndex: int = 0
    devicesLoading: bool = False
    devicesShowAll: bool = False
    devicesMessage: str = 'Finding devices...'
    firmwareMessage: str = ''
    firmwareModels: List[str] = []
    firmwareModelsIndex: int = 0
    firmwareModel: str = ''
    firmwareControllers: List[str] = []
    firmwareControllersIndex: int = 0
    firmwareController: str = ''
    firmwareVersions: List[str] = []
    firmwareVersionsIndex: int = 0
    firmwareVersion: str = ''
    firmwareOverride: bool = False
    firmwareLatest: bool = True

    @computedProperty('devices')
    def deviceItems(self) -> List[str]:
        return [device.controller.item for device in self.devices if not device.controller.unknown]

    @computedProperty('devices')
    def deviceAllItems(self) -> List[str]:
        return [device.controller.item for device in self.devices]

    def current_device(self) -> Device:
        devices = self.deviceAllItems if self.devicesShowAll else self.deviceItems

        if len(devices) == 0:
            return None

        item = devices[self.devicesIndex]
        for device in self._devices:
            if device.controller.item == item:
                return device

        return None

    @computedProperty('firmwareVersion')
    def firmwareVersionTuple(self) -> Tuple[int, ...]:
        return tuple([int(v) for v in self.firmwareVersion.strip('v').split('.')])

    def onDevicesShowAllChanged(self, showAll=True):
        self.devicesEnabled = self.devicesShowAll and len(self.deviceAllItems) > 0 or not self.devicesShowAll and len(self.deviceItems) > 0

    def onUpdateClicked(self) -> None:
        device = self.current_device()
        self.enabled = False
        api.download_and_flash_firmware(self.firmwareModel, self.firmwareController, self.firmwareVersionTuple, port=device.controller.port)
        self.enabled = True
        self.find_devices()

    def onFirmwareModelChanged(self, model=''):
        self.find_versions()

    def onFirmwareControllerChanged(self, controller=''):
        self.find_versions()

    def onDevicesIndexChanged(self, index=0):
        device = self.current_device()
        if device is not None:
            if not device.controller.unknown:
                if device.controller.up_to_date:
                    self.firmwareMessage = device.controller.name + Messages.UP_TO_DATE
                else:
                    self.firmwareMessage = device.controller.name + Messages.NEW_VERSION_AVAILABLE
                self.select_model_and_controller(device)
            else:
                self.firmwareMessage = ''

    def onFirmwareOverrideChanged(self, override=False):
        device = self.current_device()
        if not override and device is not None:
            self.select_model_and_controller(device)

    def onFirmwareLatestChanged(self, latest=False):
        if latest:
            self.firmwareVersionsIndex = 0

    def onFirmwareOpenDialogAccepted(self, firmware_file: str) -> None:
        self.enabled = False
        device = self.current_device()
        firmware_path = firmware_file.replace('file:///', '')
        api.flash_firmware(firmware_path, port=device.controller.port)
        self.enabled = True
        self.find_devices()

    def select_model_and_controller(self, device):
        self.firmwareModelsIndex = find_index(self._firmwareModels, device.controller.firmware.model.upper())
        self.firmwareControllersIndex = find_index(self._firmwareModels, device.controller.firmware.controller.upper())

    def find_models_and_controllers(self):
        self.firmwareModels.clear()
        self.firmwareModels.extend([model.upper() for model in api.get_models()])
        self.firmwareControllers.clear()
        self.firmwareControllers.extend([cont.upper() for cont in api.get_controllers()])

    def find_versions(self):
        if len(self._firmwareModels) == 0 or len(self._firmwareControllers) == 0:
            return

        versions = api.get_firmware_versions_for_model(self.firmwareModel, self.firmwareController)
        self.firmwareVersions.clear()
        self.firmwareVersions.extend([f'v{version[0]}.{version[1]}.{version[2]}' for version in versions])

    def find_devices(self):
        self.devicesMessage = Messages.FINDING_DEVICES
        self._devices.clear()
        self.devicesEnabled = False
        self.on_timeout(1, self.find_devices_worker)

    def find_devices_worker(self):
        self._devices.extend([Device(controller=cont) for cont in api.detect_controllers(include_unknown=True)])
        self.devicesMessage = Messages.NO_DEVICES_FOUND
        self.onDevicesIndexChanged()
        self.onDevicesShowAllChanged()

    def onReady(self):
        self.find_models_and_controllers()
        self.find_versions()
        self.find_devices()


def get_state():
    return State()
