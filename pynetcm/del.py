from __future__ import absolute_import
import sys
import subprocrunner
import pynetcm
from .traffic_control import TrafficControl
from ._argparse_wrapper import ArgparseWrapper
from ._common import verify_network_interface


def parse_option():
    parser = ArgparseWrapper(pynetcm.VERSION)
    
    group = parser.parser.add_argument_group("Traffic Control")
    group.add_argument(
        "--device", required=True,
        help="network device name (e.g. eth0)")

    return parser.parser.parse_args()


def main():
    
    options = parse_option()

    verify_network_interface(options.device)

    pynettc = TrafficControl(options.device)

    return pynettc.delete_tc()


if __name__ == '__main__':
    sys.exit(main())
