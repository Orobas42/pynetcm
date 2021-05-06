from __future__ import absolute_import
import sys
import dataproperty
import pyparsing as pp
import six
import subprocrunner
import pynetcm
from .traffic_control import TrafficControl
from .traffic_control import TrafficDirection
from ._argparse_wrapper import ArgparseWrapper


def parse_option():
    parser = ArgparseWrapper(pynetcm.VERSION)
    
    group = parser.parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--device",
        help="network device name (e.g. eth0)")
    group.add_argument(
        "-f", "--config-file",
        help="""setting traffic controls from a configuration file.
        output file of the tcshow.""")

    group = parser.parser.add_argument_group("Network Interface")
    group.add_argument(
        "--overwrite", action="store_true", default=False,
        help="overwrite existing settings")

    group = parser.parser.add_argument_group("Traffic Control")
    group.add_argument(
        "--direction", choices=pynetcm.traffic_control.TrafficDirection.LIST,
        default=pynetcm.traffic_control.TrafficDirection.OUTGOING,
        help="""the direction of network communication that impose traffic control.
        ``incoming`` requires linux kernel version 2.6.20 or later.
        (default = ``%(default)s``)
        """)
    group.add_argument(
        "--rate", dest="bandwidth_rate",
        help="network bandwidth rate [K|M|G bps]")
    group.add_argument(
        "--delay", dest="network_latency", type=float, default=0,
        help="round trip network delay [ms] (default=%(default)s)")
    group.add_argument(
        "--delay-distro", dest="latency_distro_ms", type=float, default=0,
        help="""
        distribution of network latency becomes X +- Y [ms]
        (normal distribution), with this option.
        (X: value of --delay option, Y: value of --delay-dist option)
        network latency distribution will be uniform without this option.
        """)
    group.add_argument(
        "--loss", dest="packet_loss_rate", type=float, default=0,
        help="round trip packet loss rate [%%] (default=%(default)s)")
    group.add_argument(
        "--corrupt", dest="corruption_rate", type=float, default=0,
        help="""
        packet corruption rate [%%]. packet corruption means single bit error
        at a random offset in the packet. (default=%(default)s)
        """)
    group.add_argument(
        "--network",
        help="IP address/network of traffic control")
    group.add_argument(
        "--port", type=int,
        help="port number of traffic control")

    return parser.parser.parse_args()


class TcConfigLoader(object):

    def __init__(self):
        self.__config_table = None
        self.is_overwrite = False

    def load_pynetcm(self, config_file_path):
        import json
        from voluptuous import Schema, Required, Any, ALLOW_EXTRA

        schema = Schema({
            Required(six.text_type): {
                Any(*TrafficDirection.LIST): {
                    six.text_type: {
                        six.text_type: six.text_type,
                    },
                }
            },
        }, extra=ALLOW_EXTRA)

        with open(config_file_path) as fp:
            self.__config_table = json.load(fp)

        schema(self.__config_table)

    def get_pynetcm_command_list(self):
        command_list = []

        for device, device_table in six.iteritems(self.__config_table):
            if self.is_overwrite:
                command_list.append("pynet-del --device " + device)

            for direction, direction_table in six.iteritems(device_table):
                for tc_filter, filter_table in six.iteritems(direction_table):
                    if filter_table == {}:
                        continue

                    option_list = [
                        "--device=" + device,
                        "--direction=" + direction,
                    ] + [
                        "--{:s}={:s}".format(k, v)
                        for k, v in six.iteritems(filter_table)
                    ]

                    try:
                        network = self.__parse_tc_filter_network(tc_filter)
                        if network != "0.0.0.0/0":
                            option_list.append("--network=" + network)
                    except pp.ParseException:
                        pass

                    try:
                        port = self.__parse_tc_filter_port(tc_filter)
                        option_list.append("--port=" + port)
                    except pp.ParseException:
                        pass

                    command_list.append(" ".join(["pynet-set"] + option_list))

        return command_list

    @staticmethod
    def __parse_tc_filter_network(text):
        network_pattern = (
            pp.SkipTo("network=", include=True) +
            pp.Word(pp.alphanums + "." + "/"))

        return network_pattern.parseString(text)[-1]

    @staticmethod
    def __parse_tc_filter_port(text):
        port_pattern = (
            pp.SkipTo("port=", include=True) +
            pp.Word(pp.nums))

        return port_pattern.parseString(text)[-1]


def main():
	
    options = parse_option()

    if dataproperty.is_not_empty_string(options.config_file):
        return_code = 0

        loader = TcConfigLoader()
        loader.is_overwrite = options.overwrite
        loader.load_pynetcm(options.config_file)

        for pynetcm_command in loader.get_pynetcm_command_list():
            return_code |= subprocrunner.SubprocessRunner(
                pynetcm_command).run()

        return return_code

    tc = TrafficControl(options.device)
    tc.direction = options.direction
    tc.bandwidth_rate = options.bandwidth_rate
    tc.latency_ms = options.network_latency
    tc.latency_distro_ms = options.latency_distro_ms
    tc.packet_loss_rate = options.packet_loss_rate
    tc.corruption_rate = options.corruption_rate
    tc.network = options.network
    tc.port = options.port

    tc.validate()

    if options.overwrite:
        tc.delete_tc()

    tc.set_tc()

    return 0


if __name__ == '__main__':
    sys.exit(main())
