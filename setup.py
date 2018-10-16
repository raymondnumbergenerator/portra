from setuptools import find_packages
from setuptools import setup

setup(
    name='portra-srv',
    version='0.1.0',
    author='Raymond Ng',
    packages=find_packages(),
    include_package_data=True,
    install_requires=(
        'flask',
        'python-xmp-toolkit',
        'Pillow',
    ),
)
