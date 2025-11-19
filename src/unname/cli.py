from .packages import get_packages
from .anonymize import anonymize_package


def main():
    packages = get_packages()
    for package in packages:
        anonymize_package(package)
