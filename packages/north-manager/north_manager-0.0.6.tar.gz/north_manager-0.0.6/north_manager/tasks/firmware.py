import logging
from invoke import task
from north_manager import api

logger = logging.getLogger(__name__)


@task(help={'model': 'Controller model (eg. n9)', 'controller': 'Override controller type (default: c9)'})
def list_versions(c, model, controller='c9'):
    """
    List available firmware versions
    """
    versions = [f'v{major}.{minor}.{patch}' for major, minor, patch in api.get_firmware_versions_for_model(model, controller)]
    for version in versions:
        logger.info(version)


@task(help={
    'model': 'Override controller model (eg. n9)',
    'controller': 'Override controller type (default: c9)',
    'version': 'Firmware version (eg. v0.1.0, defaults to latest)',
    'port': 'COM port of controller to update (eg. COM2), will only update a single controller if given',
    'ram': 'Upload firmware to RAM only instead of RAM and EEPROM (default: RAM and EEPROM)',
    'force': "Force update even if it isn't needed",
})
def update(c, model=None, version=None, controller='c9', port=None, ram=False, force=False):
    """
    Updates firmware for all connected controllers, or a single controller if a COM port is given
    """
    controllers = [api.request_controller_info(port)] if port is not None else api.detect_controllers()

    if len(controllers) == 0:
        logger.warning(f'No controllers found')
        return

    for cont in controllers:
        controller_model = model or cont.firmware.model if cont.firmware is not None else model
        controller_type = controller or cont.firmware.controller if cont.firmware is not None else controller

        if controller_model is None or controller_type is None:
            logger.error(f'Cannot update firmware please specify a controller type and model!')
            return

        if version:
            firmware_version = api.parse_version(version)
            if firmware_version is None:
                logger.error(f'Invalid firmware version: "{version}", must in vA.B.C format!')
                return
        else:
            firmware_version = api.get_latest_firmware_version_for_model(controller_model, controller_type)

        if force or (cont.firmware is not None and firmware_version > cont.firmware.version):
            logger.info(f'\n# {cont}')
            logger.info(f'Updating firmware to v{firmware_version[0]}.{firmware_version[1]}.{firmware_version[2]}')
            try:
                api.download_and_flash_firmware(controller_model, controller_type, version=firmware_version)
            except api.NorthManagerFirmwareNotFoundError:
                logger.error(f'Firmware not found!')
                return
        else:
            logger.warning(f'Firmware already latest version for "{cont}"')


@task(help={'port': 'Controller COM port (eg. COM2)'})
def info(c, port=None):
    """
    Prints firmware and port information for all connected controllers, or a single controller if a COM port is given
    """
    if port is not None:
        controller = api.request_controller_info(port)
        logger.info(f'{port}: {controller}')
    else:
        for controller in api.detect_controllers():
            logger.info(f'{controller.port}: {controller}')
