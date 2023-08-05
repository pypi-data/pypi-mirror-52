import os

import autofit as af
import autolens as al

test_path = "{}/../".format(os.path.dirname(os.path.realpath(__file__)))


def pixel_scale_from_data_resolution(data_resolution):
    """Determine the pixel scale from a instrument resolution type based on real observations.

    These options are representative of LSST, Euclid, HST, over-sampled HST and Adaptive Optics image.

    Parameters
    ----------
    data_resolution : str
        A string giving the resolution of the desired instrument type (LSST | Euclid | HST | HST_Up | AO).
    """
    if data_resolution == "LSST":
        return 0.2
    elif data_resolution == "Euclid":
        return 0.1
    elif data_resolution == "HST":
        return 0.05
    elif data_resolution == "HST_Up":
        return 0.03
    elif data_resolution == "AO":
        return 0.01
    else:
        raise ValueError(
            "An invalid instrument resolution was entered - ", data_resolution
        )


def shape_from_data_resolution(data_resolution):
    """Determine the shape of an image from a instrument resolution type based on real observations.

    These options are representative of LSST, Euclid, HST, over-sampled HST and Adaptive Optics image.

    Parameters
    ----------
    data_resolution : str
        A string giving the resolution of the desired instrument type (LSST | Euclid | HST | HST_Up | AO).
    """
    if data_resolution == "LSST":
        return (100, 100)
    elif data_resolution == "Euclid":
        return (150, 150)
    elif data_resolution == "HST":
        return (250, 250)
    elif data_resolution == "HST_Up":
        return (320, 320)
    elif data_resolution == "AO":
        return (750, 750)
    else:
        raise ValueError("An invalid instrument-type was entered - ", data_resolution)


def data_resolution_from_pixel_scale(pixel_scale):
    if pixel_scale == 0.2:
        return "LSST"
    elif pixel_scale == 0.1:
        return "Euclid"
    elif pixel_scale == 0.05:
        return "HST"
    elif pixel_scale == 0.03:
        return "HST_Up"
    elif pixel_scale == 0.01:
        return "AO"
    else:
        raise ValueError("An invalid pixel-scale was entered - ", pixel_scale)


def load_test_ccd_data(data_type, data_resolution, psf_shape=(11, 11), lens_name=None):
    pixel_scale = pixel_scale_from_data_resolution(data_resolution=data_resolution)

    data_path = af.path_util.make_and_return_path_from_path_and_folder_names(
        path=test_path, folder_names=["data", data_type, data_resolution]
    )

    return al.load_ccd_data_from_fits(
        image_path=data_path + "/image.fits",
        psf_path=data_path + "/psf.fits",
        noise_map_path=data_path + "/noise_map.fits",
        pixel_scale=pixel_scale,
        resized_psf_shape=psf_shape,
        lens_name=lens_name,
    )
