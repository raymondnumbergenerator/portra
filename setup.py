from setuptools import setup

setup(
    name='portra',
    version='0.1.0',
    author='Raymond Ng',
    packages=['portra',],
    include_package_data=True,
    install_requires=(
        'flask',
        'python-xmp-toolkit',
    ),
)
