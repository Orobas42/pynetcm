from __future__ import absolute_import
import json
import sys
import six
#import subprocrunner
import pynetcm
from .traffic_control import TrafficControl
from ._argparse_wrapper import ArgparseWrapper
from ._common import verify_network_interface


def parse_option():
    parser = ArgparseWrapper(pynetcm.VERSION)

    group = parser.parser.add_argument_group("Traffic Control")
    group.add_argument(
        "--device", action="append", required=True,
        help="network device name (e.g. eth0)")

    return parser.parser.parse_args()


def main():
    options = parse_option()

    pynettc_param = {}
    for device in options.device:
        verify_network_interface(device)

        pynettc = TrafficControl(device)
        pynettc_param.update(pynettc.get_tc_parameter())

    six.print_(json.dumps(pynettc_param, indent=4))

    return 0


if __name__ == '__main__':
    sys.exit(main())
