from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in imperium_pim/__init__.py
from imperium_pim import __version__ as version

setup(
	name="imperium_pim",
	version=version,
	description="PIM for Imperium Systems internal use",
	author="Imperium Systems & Consulting",
	author_email="wpatrickmorgan@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

