"""Setup module for zigpy-zigate"""

from setuptools import find_packages, setup
from zigpy_zigate import __version__

setup(
    name="zigpy-zigate",
    version=__version__,
    description="A library which communicates with ZiGate radios for zigpy",
    url="http://github.com/doudz/zigpy-zigate",
    author="Sébastien RAMAGE",
    author_email="sebatien.ramage@gmail.com",
    license="GPL-3.0",
    packages=find_packages(exclude=['*.tests']),
    install_requires=[
        'pyserial-asyncio',
        'zigpy-homeassistant',  # https://github.com/zigpy/zigpy/issues/190
        'RPi.GPIO',
    ],
    tests_require=[
        'pytest',
    ],
)
