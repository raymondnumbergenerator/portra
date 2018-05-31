## Portra

### Requirements
Portra uses the Python XMP Toolkit, which requires [Exempi](https://libopenraw.freedesktop.org/wiki/Exempi/) when running your own copy. Refer to the Python XMP Toolkit [documentation](https://python-xmp-toolkit.readthedocs.io/en/latest/installation.html) for further information.

### Overview
Portra is a simple Flask app that allows you to view XMP metadata stored in an image and extract it as an `.xmp` sidecar file. Portra also lets you export Adobe Camera Raw settings into a `.lrtemplate` file to be used in Adobe Lightroom.

A command line tool `portracl` is also provided that provides the same backend functionality from the command line.
