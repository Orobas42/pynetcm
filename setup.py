from __future__ import absolute_import
import setuptools

with open("require.cfg") as req:
    install_requires = [line.strip() for line in req if line.strip()]

setuptools.setup(
    name="pynetcm",
    version="0.1",
    author="vP3nguin",
    author_email="leon@vP3ngu.in",
    url="https://github.com/13loodH4t/pynetcm",
    keywords=["traffic control", "bandwidth", "latency", "packet loss"],
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "pynet-set=pynetcm.set:main",
            "pynet-del=pynetcm.del:main",
            "pynet-show=pynetcm.show:main",
        ],
    }
)
