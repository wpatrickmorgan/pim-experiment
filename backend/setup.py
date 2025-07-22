from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# Define version here instead of importing it (prevents pip install errors)
version = "0.0.1"

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

