import functools
import os
import pickle

from abc import ABC
from abc import abstractmethod
from flask import url_for
from libxmp import XMPMeta

from portra.app import app
from portra.component.lr import crs_full_all
from portra.component.xmp import exif_metadata
from portra.component.xmp import has_metadata
from portra.component.export import xmp_export_full
from portra.component.metadata import get_image_metadata
from portra.component.tags import VIGNETTE_STYLE
from portra.component.tags import PROCESS_VERSION

from portra.utils import random_filename
from portra.utils import tc_format_js

from werkzeug.utils import secure_filename

class Backend(ABC):
    """
    Abstract base class for implementing a storage backend.
    The three methods that need to be implemented are outlined here.
    """

    @abstractmethod
    def get_img_url(self, filename):
        """
        Returns a URL to the image.
        This should return None if the image does not exist.
        """
        return

    @abstractmethod
    def get_img_info(self, filename):
        """
        Returns the metadata for the image.
        This method can assume that the image exists.
        The image information should be returned as a dictionary with the following:
            filename -- original filename of the image
            xmp -- .xmp of the image stored as an XMP object
            metadata -- image metadata returned by get_image_metadata
            exif -- exif metadata returned by exif_metadata
            lightroom -- crs metadata returned by crs_full_all
        """
        return

    @abstractmethod
    def save_image(self, file):
        """
        Saves the file and returns the filename such that
        get_img_url(filename) returns the URL to this file and
        get_img_info(filename) returns the metadata to this file.
        """
        return

class FileBackend(Backend):
    """Stores files on disk."""

    IMAGES_PATH = app.config['STORAGE_BACKEND']['img_path']
    METADATA_PATH = app.config['STORAGE_BACKEND']['met_path']

    def get_img_url(self, filename):
        if os.path.isfile(self.__img_path__(filename)):
            return url_for('img', filename=filename)
        return None

    def get_img_info(self, filename):
        info_filename = filename.split('.')[0] + '.met'
        info_path = os.path.join(FileBackend.METADATA_PATH, info_filename)

        # Regenerate the metadata file if it is missing.
        if not os.path.isfile(info_path):
            info = self.__img_info__(self.__img_path__(filename))
            pickle.dump(info, \
                        open(os.path.join(FileBackend.METADATA_PATH, info_filename), 'wb'), \
                        protocol=pickle.HIGHEST_PROTOCOL)

        info = pickle.load(open(info_path, 'rb'))

        # an XMP object can't be pickled, so we serialize it when saving and
        # deserialize it when loading
        xmp = XMPMeta()
        xmp.parse_from_str(info['xmp'])
        info['xmp'] = xmp

        return info

    def save_image(self, file):
        original_filename = file.filename
        filename = random_filename(8)
        file.save(os.path.join(FileBackend.IMAGES_PATH, filename))

        info = self.__img_info__(self.__img_path__(filename))
        info['filename'] = original_filename
        info_filename = filename.split('.')[0] + '.met'
        pickle.dump(info, \
                    open(os.path.join(FileBackend.METADATA_PATH, info_filename), 'wb'), \
                    protocol=pickle.HIGHEST_PROTOCOL)

        return filename

    def __img_info__(self, file):
        xmp = xmp_export_full(file)
        metadata = get_image_metadata(file)
        lightroom = {}
        if has_metadata(xmp):
            lightroom = crs_full_all(xmp)
            lightroom['ProcessVersion'] = PROCESS_VERSION[lightroom['ProcessVersion']]
            lightroom['PostCropVignetteStyle'] = VIGNETTE_STYLE[lightroom['PostCropVignetteStyle']]
            lightroom['ToneCurvePV2012'] = tc_format_js(lightroom['ToneCurvePV2012'])
            lightroom['ToneCurvePV2012Red'] = tc_format_js(lightroom['ToneCurvePV2012Red'])
            lightroom['ToneCurvePV2012Green'] = tc_format_js(lightroom['ToneCurvePV2012Green'])
            lightroom['ToneCurvePV2012Blue'] = tc_format_js(lightroom['ToneCurvePV2012Blue'])
        exif = exif_metadata(xmp)

        return {
            'xmp': xmp.serialize_to_unicode(omit_packet_wrapper=True, use_compact_format=True),
            'metadata': metadata,
            'exif': exif,
            'lightroom': lightroom,
        }

    def __img_path__(self, filename):
        return os.path.join(self.IMAGES_PATH, filename)

@functools.lru_cache(maxsize=8)
def backend():
    return {
        'file' : FileBackend,
    }[app.config['STORAGE_BACKEND']['type']]()
