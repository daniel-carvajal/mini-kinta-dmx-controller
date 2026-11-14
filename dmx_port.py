"""Choose the USB-DMX serial port: --port, then MINIKINTA_DMX_PORT, then auto-detect."""

import argparse
import os
import sys

from serial.tools import list_ports

ENV_VAR = "MINIKINTA_DMX_PORT"
DEFAULT_PORT = "/dev/cu.usbserial-AQ02YN7D"
FTDI_VID = 0x0403


def ftdi_ports():
    return sorted((p for p in list_ports.comports() if p.vid == FTDI_VID), key=lambda p: p.device)


def resolve_port(argv=None):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--port")
    args, _ = parser.parse_known_args(sys.argv[1:] if argv is None else argv)

    if args.port:
        return args.port
    if os.environ.get(ENV_VAR):
        return os.environ[ENV_VAR]

    found = ftdi_ports()
    if len(found) == 1:
        return found[0].device
    if not found:
        return DEFAULT_PORT

    listing = "\n".join(f"  {p.device}  (serial {p.serial_number}, {p.description})" for p in found)
    duplicate = len({p.serial_number for p in found}) < len(found)
    hint = (
        "The same adapter appears more than once, which means two drivers are attached to it.\n"
        "Only one of these ports reaches the light. See 'Two ports for one adapter' in README.md.\n"
        if duplicate else ""
    )
    sys.exit(
        f"Found several FTDI serial ports:\n{listing}\n{hint}"
        f"Pick one with --port /dev/cu.xxx or {ENV_VAR}=/dev/cu.xxx"
    )
