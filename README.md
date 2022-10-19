# PyNetCM

<b>Python Network Control Manager</b>

	usage: pynet-set [-h] [--version] (--device DEVICE | -f CONFIG_FILE)
		             [--overwrite] [--direction {outgoing,incoming}]
		             [--rate BANDWIDTH_RATE] [--delay NETWORK_LATENCY]
		             [--delay-distro LATENCY_DISTRO_MS] [--loss PACKET_LOSS_RATE]
		             [--corrupt CORRUPTION_RATE] [--network NETWORK] [--port PORT]

	Optional Arguments:
	  -h, --help            show this help message and exit
	  --version             show program's version number and exit
	  --device DEVICE       network device name (e.g. eth0)
	  -f CONFIG_FILE, --config-file CONFIG_FILE
		                    setting traffic controls from a configuration file.
		                    output file of the tcshow.

	Network Interface:
	  --overwrite           overwrite existing settings

	Traffic Control:
	  --direction {outgoing,incoming}
		                    the direction of network communication that impose
		                    traffic control. ``incoming`` requires linux kernel
		                    version 2.6.20 or later. (default = ``outgoing``)
	  --rate BANDWIDTH_RATE
		                    network bandwidth rate [K|M|G bps]
	  --delay NETWORK_LATENCY
		                    round trip network delay [ms] (default=0)
	  --delay-distro LATENCY_DISTRO_MS
		                    distribution of network latency becomes X +- Y [ms]
		                    (normal distribution), with this option. (X: value of
		                    --delay option, Y: value of --delay-dist option)
		                    network latency distribution will be uniform without
		                    this option.
	  --loss PACKET_LOSS_RATE
		                    round trip packet loss rate [%] (default=0)
	  --corrupt CORRUPTION_RATE
		                    packet corruption rate [%]. packet corruption means
		                    single bit error at a random offset in the packet.
		                    (default=0)
	  --network NETWORK     IP address/network of traffic control
	  --port PORT           port number of traffic control


	  Examples:
		#pynet-set --delay 10000 --device eth0
		#pynet-set --rate 10M --port 80 --device eth0
		#pynet-set --direction incoming --loss 10 --device eth0


	usage: pynet-show [-h] [--version] --device DEVICE

	optional arguments:
	  -h, --help       show this help message and exit
	  --version        show program's version number and exit

	Traffic Control:
	  --device DEVICE  network device name (e.g. eth0)


	usage: pynet-del [-h] [--version] --device DEVICE

	optional arguments:
	  -h, --help       show this help message and exit
	  --version        show program's version number and exit

	Traffic Control:
	  --device DEVICE  network device name (e.g. eth0)

<b>Installation:</b>

	# git clone "https://github.com/vP3nguin/pynetcm.git"
	# cd pynetcm
	# sudo python setup.py build
	# sudo python setup.py install
	# sudo pynet-set -h
	# sudo pynet-show -h
	# sudo pynet-del -h

<b>Dependencies:</b>

	TrafficControl (tc)  - apt-get install iproute
	module ipaddress     - https://pypi.python.org/pypi/ipaddress
	module DataProperty  - https://pypi.python.org/pypi/DataProperty/0.8.1
	module pyparsing     - https://pypi.python.org/pypi/pyparsing/2.1.8
	module six           - https://pypi.python.org/pypi/six/1.10.0
	module subprocrunne  - https://pypi.python.org/pypi/subprocrunner/0.4.0
	module voluptuou     - https://pypi.python.org/pypi/voluptuous

<b>In Progress:</b>

	- add packet duplication


