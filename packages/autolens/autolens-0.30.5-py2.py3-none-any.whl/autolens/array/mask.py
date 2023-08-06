import logging

import numpy as np

from autolens import exc
from autolens.array.util import grid_util, array_util, mask_util, binning_util
from autolens.array.mapping_util import (
    array_mapping_util,
    grid_mapping_util,
    mask_mapping_util,
)
from autolens.array import scaled_array

logging.basicConfig()
logger = logging.getLogger(__name__)


class Mask(scaled_array.ScaledSquarePixelArray):
    """
    A mask represented by an ndarray where True is masked.
    """

    # noinspection PyUnusedLocal
    def __init__(self, array, pixel_scale, origin=(0.0, 0.0)):
        """ A mask, which is applied to a 2D array of hyper_galaxies to extract a set of unmasked image pixels (i.e. mask entry \
        is *False* or 0) which are then fitted in an analysis.
        
        The mask retains the pixel scale of the array and has a centre and origin.
        
        Parameters
        ----------
        array: ndarray
            An array of bools representing the mask.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        origin : (float, float)
            The (y,x) arc-second origin of the mask's coordinate system.
        centre : (float, float)
            The (y,x) arc-second centre of the mask provided it is a standard geometric shape (e.g. a circle).
        """
        # noinspection PyArgumentList
        super(Mask, self).__init__(array=array, pixel_scale=pixel_scale, origin=origin)

    def __array_finalize__(self, obj):
        if hasattr(obj, "pixel_scale"):
            self.pixel_scale = obj.pixel_scale
        if hasattr(obj, "origin"):
            self.origin = obj.origin
        if hasattr(obj, "origin"):
            self.origin = obj.origin

    def __getitem__(self, coords):
        try:
            return super(Mask, self).__getitem__(coords)
        except IndexError:
            return True

    @classmethod
    def unmasked_for_shape_and_pixel_scale(cls, shape, pixel_scale, invert=False):
        """Setup a mask where all pixels are unmasked.

        Parameters
        ----------
        shape : (int, int)
            The (y,x) shape of the mask in units of pixels.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        """
        mask = np.full(tuple(map(lambda d: int(d), shape)), False)
        if invert:
            mask = np.invert(mask)
        return cls(array=mask, pixel_scale=pixel_scale)

    @classmethod
    def circular(
        cls, shape, pixel_scale, radius_arcsec, centre=(0.0, 0.0), invert=False
    ):
        """Setup a mask where unmasked pixels are within a circle of an input arc second radius and centre.

        Parameters
        ----------
        shape: (int, int)
            The (y,x) shape of the mask in units of pixels.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        radius_arcsec : float
            The radius (in arc seconds) of the circle within which pixels unmasked.
        centre: (float, float)
            The centre of the circle used to mask pixels.
        """
        mask = mask_util.mask_circular_from_shape_pixel_scale_and_radius(
            shape=shape,
            pixel_scale=pixel_scale,
            radius_arcsec=radius_arcsec,
            centre=centre,
        )
        if invert:
            mask = np.invert(mask)
        return cls(array=mask.astype("bool"), pixel_scale=pixel_scale)

    @classmethod
    def circular_annular(
        cls,
        shape,
        pixel_scale,
        inner_radius_arcsec,
        outer_radius_arcsec,
        centre=(0.0, 0.0),
        invert=False,
    ):
        """Setup a mask where unmasked pixels are within an annulus of input inner and outer arc second radii and \
         centre.

        Parameters
        ----------
        shape : (int, int)
            The (y,x) shape of the mask in units of pixels.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        inner_radius_arcsec : float
            The radius (in arc seconds) of the inner circle outside of which pixels are unmasked.
        outer_radius_arcsec : float
            The radius (in arc seconds) of the outer circle within which pixels are unmasked.
        centre: (float, float)
            The centre of the annulus used to mask pixels.
        """

        mask = mask_util.mask_circular_annular_from_shape_pixel_scale_and_radii(
            shape=shape,
            pixel_scale=pixel_scale,
            inner_radius_arcsec=inner_radius_arcsec,
            outer_radius_arcsec=outer_radius_arcsec,
            centre=centre,
        )

        if invert:
            mask = np.invert(mask)

        return cls(array=mask.astype("bool"), pixel_scale=pixel_scale)

    @classmethod
    def circular_anti_annular(
        cls,
        shape,
        pixel_scale,
        inner_radius_arcsec,
        outer_radius_arcsec,
        outer_radius_2_arcsec,
        centre=(0.0, 0.0),
        invert=False,
    ):
        """Setup a mask where unmasked pixels are outside an annulus of input inner and outer arc second radii, but \
        within a second outer radius, and at a given centre.

        This mask there has two distinct unmasked regions (an inner circle and outer annulus), with an inner annulus \
        of masked pixels.

        Parameters
        ----------
        shape : (int, int)
            The (y,x) shape of the mask in units of pixels.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        inner_radius_arcsec : float
            The radius (in arc seconds) of the inner circle inside of which pixels are unmasked.
        outer_radius_arcsec : float
            The radius (in arc seconds) of the outer circle within which pixels are masked and outside of which they \
            are unmasked.
        outer_radius_2_arcsec : float
            The radius (in arc seconds) of the second outer circle within which pixels are unmasked and outside of \
            which they masked.
        centre: (float, float)
            The centre of the anti-annulus used to mask pixels.
        """

        mask = mask_util.mask_circular_anti_annular_from_shape_pixel_scale_and_radii(
            shape=shape,
            pixel_scale=pixel_scale,
            inner_radius_arcsec=inner_radius_arcsec,
            outer_radius_arcsec=outer_radius_arcsec,
            outer_radius_2_arcsec=outer_radius_2_arcsec,
            centre=centre,
        )

        if invert:
            mask = np.invert(mask)

        return cls(array=mask.astype("bool"), pixel_scale=pixel_scale)

    @classmethod
    def elliptical(
        cls,
        shape,
        pixel_scale,
        major_axis_radius_arcsec,
        axis_ratio,
        phi,
        centre=(0.0, 0.0),
        invert=False,
    ):
        """ Setup a mask where unmasked pixels are within an ellipse of an input arc second major-axis and centre.

        Parameters
        ----------
        shape: (int, int)
            The (y,x) shape of the mask in units of pixels.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        major_axis_radius_arcsec : float
            The major-axis (in arc seconds) of the ellipse within which pixels are unmasked.
        axis_ratio : float
            The axis-ratio of the ellipse within which pixels are unmasked.
        phi : float
            The rotation angle of the ellipse within which pixels are unmasked, (counter-clockwise from the positive \
             x-axis).
        centre: (float, float)
            The centre of the ellipse used to mask pixels.
        """

        mask = mask_util.mask_elliptical_from_shape_pixel_scale_and_radius(
            shape, pixel_scale, major_axis_radius_arcsec, axis_ratio, phi, centre
        )

        if invert:
            mask = np.invert(mask)

        return cls(array=mask.astype("bool"), pixel_scale=pixel_scale)

    @classmethod
    def elliptical_annular(
        cls,
        shape,
        pixel_scale,
        inner_major_axis_radius_arcsec,
        inner_axis_ratio,
        inner_phi,
        outer_major_axis_radius_arcsec,
        outer_axis_ratio,
        outer_phi,
        centre=(0.0, 0.0),
        invert=False,
    ):
        """Setup a mask where unmasked pixels are within an elliptical annulus of input inner and outer arc second \
        major-axis and centre.

        Parameters
        ----------
        shape: (int, int)
            The (y,x) shape of the mask in units of pixels.
        pixel_scale: float
            The arc-second to pixel conversion factor of each pixel.
        inner_major_axis_radius_arcsec : float
            The major-axis (in arc seconds) of the inner ellipse within which pixels are masked.
        inner_axis_ratio : float
            The axis-ratio of the inner ellipse within which pixels are masked.
        inner_phi : float
            The rotation angle of the inner ellipse within which pixels are masked, (counter-clockwise from the \
            positive x-axis).
        outer_major_axis_radius_arcsec : float
            The major-axis (in arc seconds) of the outer ellipse within which pixels are unmasked.
        outer_axis_ratio : float
            The axis-ratio of the outer ellipse within which pixels are unmasked.
        outer_phi : float
            The rotation angle of the outer ellipse within which pixels are unmasked, (counter-clockwise from the \
            positive x-axis).
        centre: (float, float)
            The centre of the elliptical annuli used to mask pixels.
        """

        mask = mask_util.mask_elliptical_annular_from_shape_pixel_scale_and_radius(
            shape=shape,
            pixel_scale=pixel_scale,
            inner_major_axis_radius_arcsec=inner_major_axis_radius_arcsec,
            inner_axis_ratio=inner_axis_ratio,
            inner_phi=inner_phi,
            outer_major_axis_radius_arcsec=outer_major_axis_radius_arcsec,
            outer_axis_ratio=outer_axis_ratio,
            outer_phi=outer_phi,
            centre=centre,
        )

        if invert:
            mask = np.invert(mask)

        return cls(array=mask.astype("bool"), pixel_scale=pixel_scale)

    def binned_up_mask_from_mask(self, bin_up_factor):

        binned_up_mask = binning_util.binned_up_mask_2d_from_mask_2d_and_bin_up_factor(
            mask_2d=self, bin_up_factor=bin_up_factor
        )

        return Mask(
            array=binned_up_mask,
            pixel_scale=self.pixel_scale * bin_up_factor,
            origin=self.origin,
        )

    @property
    @array_util.Memoizer()
    def centre(self):
        return grid_util.grid_centre_from_grid_1d(grid_1d=self.masked_grid_1d)

    @property
    def pixels_in_mask(self):
        return int(np.size(self) - np.sum(self))

    @property
    def mask_1d_index_to_mask_2d_index(self):
        """A 1D array of mappings between every unmasked pixel and its 2D pixel coordinates."""
        return self.sub_mask_1d_index_to_sub_mask_2d_index_from_sub_grid_size(
            sub_grid_size=1
        )

    def sub_mask_1d_index_to_sub_mask_2d_index_from_sub_grid_size(self, sub_grid_size):
        """A 1D array of mappings between every unmasked sub pixel and its 2D sub-pixel coordinates."""
        return mask_mapping_util.sub_mask_1d_index_to_sub_mask_2d_index_from_mask_and_sub_grid_size(
            mask=self, sub_grid_size=sub_grid_size
        ).astype(
            "int"
        )

    def array_1d_from_array_2d(self, array_2d):
        """For a 2D array (e.g. an image, noise_map, etc.) map it to a masked 1D array of valuees using this mask.

        Parameters
        ----------
        array_2d : ndarray | None | float
            The 2D array to be mapped to a masked 1D array.
        """
        if array_2d is None or isinstance(array_2d, float):
            return array_2d
        return array_mapping_util.sub_array_1d_from_sub_array_2d_mask_and_sub_grid_size(
            mask=self, sub_array_2d=array_2d, sub_grid_size=1
        )

    def array_2d_from_array_1d(self, array_1d):
        """ Map a 1D array the same dimension as the grid to its original 2D array.

        Values which were masked in the mapping_util to the 1D array are returned as zeros.

        Parameters
        -----------
        array_1d : ndarray
            The 1D array which is mapped to its masked 2D array.
        """
        return array_mapping_util.sub_array_2d_from_sub_array_1d_mask_and_sub_grid_size(
            sub_array_1d=array_1d, mask=self, sub_grid_size=1
        )

    def scaled_array_2d_from_array_1d(self, array_1d):
        """ Map a 1D array the same dimension as the grid to its original masked 2D array and return it as a hyper \
        array.

        Parameters
        -----------
        array_1d : ndarray
            The 1D array of which is mapped to a 2D hyper array.
        """
        return scaled_array.ScaledSquarePixelArray(
            array=self.array_2d_from_array_1d(array_1d=array_1d),
            pixel_scale=self.pixel_scale,
            origin=self.origin,
        )

    def grid_2d_from_grid_1d(self, grid_1d):
        """Map a 1D grid the same dimension as the grid to its original 2D grid.

        Values which were masked in the mapping_util to the 1D array are returned as zeros.

        Parameters
        -----------
        grid_1d : ndarray
            The 1D grid which is mapped to its masked 2D array.
        """
        return grid_mapping_util.sub_grid_2d_from_sub_grid_1d_mask_and_sub_grid_size(
            sub_grid_1d=grid_1d, mask=self, sub_grid_size=1
        )

    def grid_1d_from_grid_2d(self, grid_2d):
        """ Map a 2D grid to its masked 1D grid..

        Values which are masked in the mapping_util to the 1D grid are returned as zeros.

        Parameters
        -----------
        grid_1d : ndgrid
            The 1D grid which is mapped to its masked 2D grid.
        """
        return grid_mapping_util.sub_grid_1d_from_sub_grid_2d_mask_and_sub_grid_size(
            sub_grid_2d=grid_2d, mask=self, sub_grid_size=1
        )

    def sub_array_2d_from_sub_array_1d_and_sub_grid_size(
        self, sub_array_1d, sub_grid_size
    ):
        """ Map a 1D sub-array the same dimension as the sub-grid (e.g. including sub-pixels) to its original masked
        2D sub array.

        Parameters
        -----------
        sub_array_1d : ndarray
            The 1D sub_array which is mapped to its masked 2D sub-array.
        """
        return array_mapping_util.sub_array_2d_from_sub_array_1d_mask_and_sub_grid_size(
            sub_array_1d=sub_array_1d, mask=self, sub_grid_size=sub_grid_size
        )

    def scaled_array_2d_with_sub_dimensions_from_sub_array_1d_and_sub_grid_size(
        self, sub_array_1d, sub_grid_size
    ):
        """ Map a 1D sub-array the same dimension as the sub-grid to its original masked 2D sub-array and return it as
        a hyper array.

        Parameters
        -----------
        sub_array_1d : ndarray
            The 1D sub-array of which is mapped to a 2D hyper sub-array the dimensions.
        """
        return scaled_array.ScaledSquarePixelArray(
            array=self.sub_array_2d_from_sub_array_1d_and_sub_grid_size(
                sub_array_1d=sub_array_1d, sub_grid_size=sub_grid_size
            ),
            pixel_scale=self.pixel_scale / sub_grid_size,
            origin=self.origin,
        )

    def array_1d_binned_from_sub_array_1d_and_sub_grid_size(
        self, sub_array_1d, sub_grid_size
    ):
        """For an input 1D sub-array, map its values to a 1D array of values by summing each set \of sub-pixel \
        values and dividing by the total number of sub-pixels.

        Parameters
        -----------
        sub_array_1d : ndarray
            A 1D sub-array of values (e.g. image, convergence, potential) which is mapped to
            a 1d array.
        """

        sub_grid_length = int(sub_grid_size ** 2.0)
        sub_grid_fraction = 1.0 / sub_grid_length

        return np.multiply(
            sub_grid_fraction, sub_array_1d.reshape(-1, sub_grid_length).sum(axis=1)
        )

    def scaled_array_2d_binned_from_sub_array_1d_and_sub_grid_size(
        self, sub_array_1d, sub_grid_size
    ):
        """ Map a 1D sub-array the same dimension as the sub-grid to its original masked 2D sub-array and return it as
        a hyper array.

        Parameters
        -----------
        sub_array_1d : ndarray
            The 1D sub-array of which is mapped to a 2D hyper sub-array the dimensions.
        """

        array_1d = self.array_1d_binned_from_sub_array_1d_and_sub_grid_size(
            sub_array_1d=sub_array_1d, sub_grid_size=sub_grid_size
        )

        return scaled_array.ScaledSquarePixelArray(
            array=self.array_2d_from_array_1d(array_1d=array_1d),
            pixel_scale=self.pixel_scale,
            origin=self.origin,
        )

    def sub_array_1d_with_sub_dimensions_from_sub_array_2d_and_sub_grid_size(
        self, sub_array_2d, sub_grid_size
    ):
        """ Map a 2D sub-array to its masked 1D sub-array.

        Values which are masked in the mapping_util to the 1D array are returned as zeros.

        Parameters
        -----------
        su_array_2d : ndarray
            The 2D sub-array which is mapped to its masked 1D sub-array.
        """
        return array_mapping_util.sub_array_1d_from_sub_array_2d_mask_and_sub_grid_size(
            sub_array_2d=sub_array_2d, mask=self, sub_grid_size=sub_grid_size
        )

    def sub_grid_1d_with_sub_dimensions_from_sub_grid_2d_and_sub_grid_size(
        self, sub_grid_2d, sub_grid_size
    ):
        """For an input 1D sub-array, map its values to a 1D array of values by summing each set \of sub-pixel \
        values and dividing by the total number of sub-pixels.

        Parameters
        -----------
        sub_grid_2d : ndarray
            A 1D sub-array of values (e.g. image, convergence, potential) which is mapped to
            a 1d array.
        """
        return grid_mapping_util.sub_grid_1d_from_sub_grid_2d_mask_and_sub_grid_size(
            sub_grid_2d=sub_grid_2d, mask=self, sub_grid_size=sub_grid_size
        )

    def grid_1d_binned_from_sub_grid_1d_and_sub_grid_size(
        self, sub_grid_1d, sub_grid_size
    ):
        """For an input 1D sub-array, map its values to a 1D array of values by summing each set \of sub-pixel \
        values and dividing by the total number of sub-pixels.

        Parameters
        -----------
        sub_grid_1d : ndarray
            A 1D sub-array of values (e.g. image, convergence, potential) which is mapped to
            a 1d array.
        """

        grid_1d_y = self.array_1d_binned_from_sub_array_1d_and_sub_grid_size(
            sub_array_1d=sub_grid_1d[:, 0], sub_grid_size=sub_grid_size
        )

        grid_1d_x = self.array_1d_binned_from_sub_array_1d_and_sub_grid_size(
            sub_array_1d=sub_grid_1d[:, 1], sub_grid_size=sub_grid_size
        )

        return np.stack((grid_1d_y, grid_1d_x), axis=-1)

    def grid_2d_binned_from_sub_grid_1d_and_sub_grid_size(
        self, sub_grid_1d, sub_grid_size
    ):
        """For an input 1D sub-array, map its values to a 1D array of values by summing each set \of sub-pixel \
        values and dividing by the total number of sub-pixels.

        Parameters
        -----------
        sub_grid_1d : ndarray
            A 1D sub-array of values (e.g. image, convergence, potential) which is mapped to
            a 1d array.
        """

        grid_1d = self.grid_1d_binned_from_sub_grid_1d_and_sub_grid_size(
            sub_grid_1d=sub_grid_1d, sub_grid_size=sub_grid_size
        )

        return self.grid_2d_from_grid_1d(grid_1d=grid_1d)

    def sub_grid_2d_with_sub_dimensions_from_sub_grid_1d_and_sub_grid_size(
        self, sub_grid_1d, sub_grid_size
    ):
        """ Map a 1D sub-grid the same dimension as the sub-grid (e.g. including sub-pixels) to its original masked
        2D sub grid.

        Parameters
        -----------
        sub_grid_1d : ndgrid
            The 1D grid which is mapped to its masked 2D sub-grid.
        """
        return grid_mapping_util.sub_grid_2d_from_sub_grid_1d_mask_and_sub_grid_size(
            sub_grid_1d=sub_grid_1d, mask=self, sub_grid_size=sub_grid_size
        )

    @array_util.Memoizer()
    def sub_mask_1d_index_to_mask_1d_index_from_sub_grid_size(self, sub_grid_size):
        """The mapping_util between every sub-pixel and its host pixel.

        For example:

        - sub_to_pixel[8] = 2 -  The ninth sub-pixel is within the 3rd pixel.
        - sub_to_pixel[20] = 4 -  The twenty first sub-pixel is within the 5th pixel.
        """
        return mask_mapping_util.sub_mask_1d_index_to_mask_1d_index_from_mask(
            mask=self, sub_grid_size=sub_grid_size
        ).astype("int")

    @array_util.Memoizer()
    def blurring_mask_from_psf_shape(self, psf_shape):
        """Compute a blurring mask, which represents all masked pixels whose light will be blurred into unmasked \
        pixels via PSF convolution (see grid.Grid.blurring_grid_from_mask_and_psf_shape).

        Parameters
        ----------
        psf_shape : (int, int)
           The shape of the psf which defines the blurring region (e.g. the shape of the PSF)
        """

        if psf_shape[0] % 2 == 0 or psf_shape[1] % 2 == 0:
            raise exc.MaskException("psf_size of exterior region must be odd")

        blurring_mask = mask_util.blurring_mask_from_mask_and_psf_shape(self, psf_shape)

        return Mask(array=blurring_mask, pixel_scale=self.pixel_scale)

    @property
    def edge_1d_indexes(self):
        """The indicies of the mask's edge pixels, where an edge pixel is any unmasked pixel on its edge \
        (next to at least one pixel with a *True* value).
        """
        return mask_util.edge_1d_indexes_from_mask(mask=self).astype("int")

    @property
    def border_1d_indexes(self):
        """The indicies of the mask's border pixels, where a border pixel is any unmasked pixel on an
        exterior edge (e.g. next to at least one pixel with a *True* value but not central pixels like those within \
        an annulus mask).
        """
        return mask_util.border_1d_indexes_from_mask(mask=self).astype("int")

    @property
    def border_grid_1d(self):
        """The indicies of the mask's border pixels, where a border pixel is any unmasked pixel on an
        exterior edge (e.g. next to at least one pixel with a *True* value but not central pixels like those within \
        an annulus mask).
        """
        return self.masked_grid_1d[self.border_1d_indexes]

    def sub_border_1d_indexes_from_sub_grid_size(self, sub_grid_size, filter_size=None):
        """The indicies of the mask's border pixels, where a border pixel is any unmasked pixel on an
        exterior edge (e.g. next to at least one pixel with a *True* value but not central pixels like those within \
        an annulus mask).
        """
        sub_border_1d_indexes = mask_util.sub_border_pixel_1d_indexes_from_mask_and_sub_grid_size(
            mask=self, sub_grid_size=sub_grid_size
        ).astype(
            "int"
        )

        if filter_size is None:
            return sub_border_1d_indexes
        else:
            sub_border_thetas_1d = self.sub_border_thetas_1d_from_sub_grid_size(
                sub_grid_size=sub_grid_size
            )
            sub_border_ordered_indexes = np.argsort(sub_border_thetas_1d)
            return np.sort(
                sub_border_1d_indexes[sub_border_ordered_indexes[1::filter_size]]
            )

    def sub_border_grid_1d_from_sub_grid_size(self, sub_grid_size, filter_size=None):
        """The indicies of the mask's border pixels, where a border pixel is any unmasked pixel on an
        exterior edge (e.g. next to at least one pixel with a *True* value but not central pixels like those within \
        an annulus mask).
        """
        masked_sub_grid_1d = self.masked_sub_grid_1d_from_sub_grid_size(
            sub_grid_size=sub_grid_size
        )
        sub_border_pixel_1d_indexes = self.sub_border_1d_indexes_from_sub_grid_size(
            sub_grid_size=sub_grid_size, filter_size=filter_size
        )
        return masked_sub_grid_1d[sub_border_pixel_1d_indexes]

    def sub_border_thetas_1d_from_sub_grid_size(self, sub_grid_size, filter_size=None):
        sub_border_grid_1d = self.sub_border_grid_1d_from_sub_grid_size(
            sub_grid_size=sub_grid_size, filter_size=filter_size
        )
        return np.arctan2(
            (sub_border_grid_1d[:, 0] - self.centre[0]),
            sub_border_grid_1d[:, 1] - self.centre[1],
        )

    @property
    def masked_grid_1d(self):
        return grid_util.grid_1d_from_mask_pixel_scales_sub_grid_size_and_origin(
            mask=self,
            pixel_scales=self.pixel_scales,
            sub_grid_size=1,
            origin=self.origin,
        )

    def masked_sub_grid_1d_from_sub_grid_size(self, sub_grid_size):
        return grid_util.grid_1d_from_mask_pixel_scales_sub_grid_size_and_origin(
            mask=self,
            pixel_scales=self.pixel_scales,
            sub_grid_size=sub_grid_size,
            origin=self.origin,
        )

    @property
    def zoom_centre(self):
        extraction_grid_1d = self.grid_arcsec_to_grid_pixels(
            grid_arcsec=self.masked_grid_1d
        )
        y_pixels_max = np.max(extraction_grid_1d[:, 0])
        y_pixels_min = np.min(extraction_grid_1d[:, 0])
        x_pixels_max = np.max(extraction_grid_1d[:, 1])
        x_pixels_min = np.min(extraction_grid_1d[:, 1])
        return (
            ((y_pixels_max + y_pixels_min - 1.0) / 2.0),
            ((x_pixels_max + x_pixels_min - 1.0) / 2.0),
        )

    @property
    def zoom_offset_pixels(self):
        return (
            self.zoom_centre[0] - self.central_pixel_coordinates[0],
            self.zoom_centre[1] - self.central_pixel_coordinates[1],
        )

    @property
    def zoom_offset_arcsec(self):
        return (
            -self.pixel_scale * self.zoom_offset_pixels[0],
            self.pixel_scale * self.zoom_offset_pixels[1],
        )

    @property
    def zoom_region(self):
        """The zoomed rectangular region corresponding to the square encompassing all unmasked values. This zoomed
        extraction region is a squuare, even if the mask is rectangular.

        This is used to zoom in on the region of an image that is used in an analysis for visualization."""

        # Have to convert mask to bool for invert function to work.
        where = np.array(np.where(np.invert(self.astype("bool"))))
        y0, x0 = np.amin(where, axis=1)
        y1, x1 = np.amax(where, axis=1)

        ylength = y1 - y0
        xlength = x1 - x0

        if ylength > xlength:
            length_difference = ylength - xlength
            x1 += int(length_difference / 2.0)
            x0 -= int(length_difference / 2.0)
        elif xlength > ylength:
            length_difference = xlength - ylength
            y1 += int(length_difference / 2.0)
            y0 -= int(length_difference / 2.0)

        return [y0, y1 + 1, x0, x1 + 1]


def load_mask_from_fits(mask_path, pixel_scale, mask_hdu=0):
    return Mask.from_fits_with_pixel_scale(
        file_path=mask_path, hdu=mask_hdu, pixel_scale=pixel_scale
    )


def output_mask_to_fits(mask, mask_path, overwrite=False):
    array_util.numpy_array_2d_to_fits(
        array_2d=mask, file_path=mask_path, overwrite=overwrite
    )
