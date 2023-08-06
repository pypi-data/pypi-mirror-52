import logging


def print_header(text):
    print('#', text)


def print_firmware_info(info, prefix=''):
    controller, model, variant, major, minor, patch = info
    variant_str = '-' + variant if variant is not None else ''
    print(f'{prefix}North {controller}-{model}{variant_str}, v{major}.{minor}.{patch}')
