from setuptools import setup, find_packages

setup(
    name="iotile_support_firm_gpiopipe_1",
    packages=find_packages(include=["iotile_support_firm_gpiopipe_1.*", "iotile_support_firm_gpiopipe_1"]),
    version="1.2.0",
    install_requires=[],
    entry_points={'iotile.proxy': ['gpiopipe_proxy = iotile_support_firm_gpiopipe_1.gpiopipe_proxy']},
    include_package_data=True,
    author="Arch",
    author_email="info@arch-iot.com"
)