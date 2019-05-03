## Portra

### Requirements
Portra uses the Python XMP Toolkit, which requires [Exempi](https://libopenraw.freedesktop.org/wiki/Exempi/) when running your own copy. Refer to the Python XMP Toolkit [documentation](https://python-xmp-toolkit.readthedocs.io/en/latest/installation.html) for further information.

### Overview
Portra is a simple Flask app that allows photography enthusiasts to share photos between each other. Portra stores full-resolution images and displays XMP, Adobe Camera Raw and Adobe Lightroom metadata so settings can be shared easily.

Portra also allows for exporting of XMP metadata into an `.xmp` sidecar file, tone curves from an image into a tone curve `.xmp` file and Adobe Lightroom settings into a `.lrtemplate` file for use in Adobe Lightroom.

### Screenshots
![](https://github.com/raymondnumbergenerator/portra/raw/master/portra/static/images/screenshots/ss_basic.png)

![](https://github.com/raymondnumbergenerator/portra/raw/master/portra/static/images/screenshots/ss_detailed.png)

![](https://github.com/raymondnumbergenerator/portra/raw/master/portra/static/images/screenshots/ss_lightroom.png)

![](https://github.com/raymondnumbergenerator/portra/raw/master/portra/static/images/screenshots/ss_tc.png)

### Development Setup
1. Fork this repository and clone your fork.
2. Add this repository as the upstream remote with `git remote add upstream https://github.com/raymondnumbergenerator/portra.git`
3. `make venv` will set up the virtual environment.
4. Configure `settings.py` in settings.
5. `make dev` will run the development copy.

### Deployment Setup
1. Configure `settings.py` or create a new configuration.
2. Configure the Dockerfile if needed (for example, to use a different setting configuration).
3. Run `make docker-redeploy`.
