#!/usr/bin/env python3

import os
import sys
import glob
import subprocess


def get_usb_devices():
    usb_devices = []
    usb_devs = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
    for dev in usb_devs:
        device_type = os.path.basename(dev)[:3]
        usb_devices.append({'device': dev, 'type': device_type})

    return usb_devices


def get_device_info(device_path):
    manufacturer = subprocess.check_output(f'udevadm info --query=property \
    --name={device_path} | grep "ID_VENDOR=" | cut -d "=" \
    -f2', shell=True).decode('utf-8').strip()
    model = subprocess.check_output(f'udevadm info --query=property \
    --name={device_path} | grep "ID_MODEL=" | cut -d "=" \
    -f2', shell=True).decode('utf-8').strip()
    serial_number = subprocess.check_output(f'udevadm info --query=property \
    --name={device_path} | grep "ID_SERIAL=" | cut -d "=" \
    -f2', shell=True).decode('utf-8').strip()
    bus_number = subprocess.check_output(f'udevadm info --query=property \
    --name={device_path} | grep "ID_BUS=" | cut -d "=" \
    -f2', shell=True).decode('utf-8').strip()
    device_number = subprocess.check_output(f'udevadm info --query=property \
    --name={device_path} | grep "ID_PATH_TAG=" | cut -d "=" \
    -f2', shell=True).decode('utf-8').strip()
    device_id = subprocess.check_output(f'udevadm info --query=property \
    --name={device_path} | grep "ID_MODEL_ID=" | cut -d "=" \
    -f2', shell=True).decode('utf-8').strip()
    device_info = {
        'manufacturer': manufacturer,
        'model': model,
        'serial_number': serial_number,
        'bus_number': bus_number,
        'device_number': device_number,
        'device_id': device_id
    }
    return device_info


def lsusb_grep(id_str):
    command = "lsusb | grep " + id_str
    val = subprocess.check_output(command, shell=True)
    value = str(val, encoding="utf-8")
    return value


def main():
    devices = get_usb_devices()
    for device in devices:
        print(f"Device: {device['device']}, Type: {device['type']}")
        device_str = str({device['device']})
        device_str = device_str.replace("{", "")
        device_str = device_str.replace("}", "")
        info = get_device_info(device_str)
        print(f"Manufacturer: {info['manufacturer']}")
        print(f"Model: {info['model']}")
        print(f"Serial Number: {info['serial_number']}")
        print(f"Bus Number: {info['bus_number']}")
        print(f"Device Number: {info['device_number']}")
        print(f"Device ID: {info['device_id']}")
        id_str = str({info['device_id']})
        id_str = id_str.replace("{", "")
        id_str = id_str.replace("}", "")
        id_str = id_str.replace("'", "")
        val = lsusb_grep(id_str)
        print(val)


if __name__ == '__main__':
    sys.exit(main())
