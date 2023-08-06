from setuptools import setup

setup(
    name='uhf-rfid-reader-sdk',
    version='0.0.0',
    author="Rifqi Khoeruman Azam",
    author_email="pravodev@gmail.com",
    description="(Unofficial) UHF RFID Reader SDK",
    long_description=open('README.md').read(),
    license="MIT",
    keywords="rfid sdk",
    url="https://github.com/pravodev/uhf-rfid-reader-sdk",
    packages=['rfid_reader'],
    install_requires=[
        "crcmod==1.7",
        "pyserial==3.4",
    ]
)