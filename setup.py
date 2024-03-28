from setuptools import setup

setup(
    install_requires=[
    ],
    packages=["SetUp"],
    include_package_data=True,
    entry_points={"console_scripts": ["realpython=SetUp.main:main"]},
)
