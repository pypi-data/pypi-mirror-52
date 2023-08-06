from itertools import count

import numpy as np
from astropy import cosmology as cosmo
from skimage import measure

import autofit as af

from autolens import exc, dimensions as dim
from autolens import text_util
from autolens.model.inversion import pixelizations as pix
from autolens.model.profiles import light_profiles as lp
from autolens.model.profiles import mass_profiles as mp

from autolens.array.grids import (
    reshape_array_from_grid,
    reshape_array_from_grid_and_convolver,
    reshape_array_from_grid_and_psf,
    reshape_returned_grid,
)


def is_light_profile(obj):
    return isinstance(obj, lp.LightProfile)


def is_mass_profile(obj):
    return isinstance(obj, mp.MassProfile)


class Galaxy(af.ModelObject):
    """
    @DynamicAttrs
    """

    def __init__(
        self,
        redshift,
        pixelization=None,
        regularization=None,
        hyper_galaxy=None,
        **kwargs
    ):
        """Class representing a galaxy, which is composed of attributes used for fitting hyper_galaxies (e.g. light profiles, \
        mass profiles, pixelizations, etc.).
        
        All *has_* methods retun *True* if galaxy has that attribute, *False* if not.

        Parameters
        ----------
        redshift: float
            The redshift of the galaxy.
        light_profiles: [lp.LightProfile]
            A list of the galaxy's light profiles.
        mass_profiles: [mp.MassProfile]
            A list of the galaxy's mass profiles.
        hyper_galaxy : HyperGalaxy
            The hyper_galaxies-parameters of the hyper_galaxies-galaxy, which is used for performing a hyper_galaxies-analysis on the noise-map.
            
        Attributes
        ----------
        pixelization : inversion.Pixelization
            The pixelization of the galaxy used to reconstruct an observed image using an inversion.
        regularization : inversion.Regularization
            The regularization of the pixel-grid used to reconstruct an observed using an inversion.
        """
        super().__init__()
        self.redshift = redshift

        self.hyper_model_image_1d = (
            kwargs["hyper_model_image_1d"] if "hyper_model_image_1d" in kwargs else None
        )
        self.hyper_galaxy_image_1d = (
            kwargs["hyper_galaxy_image_1d"]
            if "hyper_galaxy_image_1d" in kwargs
            else None
        )
        self.binned_hyper_galaxy_image_1d = (
            kwargs["binned_hyper_galaxy_image_1d"]
            if "binned_hyper_galaxy_image_1d" in kwargs
            else None
        )

        for name, val in kwargs.items():
            setattr(self, name, val)

        self.pixelization = pixelization
        self.regularization = regularization

        if pixelization is not None and regularization is None:
            raise exc.GalaxyException(
                "If the galaxy has a pixelization, it must also have a regularization."
            )
        if pixelization is None and regularization is not None:
            raise exc.GalaxyException(
                "If the galaxy has a regularization, it must also have a pixelization."
            )

        self.hyper_galaxy = hyper_galaxy

    def __hash__(self):
        return self.id

    @property
    def light_profiles(self):
        return [value for value in self.__dict__.values() if is_light_profile(value)]

    @property
    def mass_profiles(self):
        return [value for value in self.__dict__.values() if is_mass_profile(value)]

    @property
    def has_redshift(self):
        return self.redshift is not None

    @property
    def has_pixelization(self):
        return self.pixelization is not None

    @property
    def has_regularization(self):
        return self.regularization is not None

    @property
    def has_hyper_galaxy(self):
        return self.hyper_galaxy is not None

    @property
    def has_light_profile(self):
        return len(self.light_profiles) > 0

    @property
    def has_mass_profile(self):
        return len(self.mass_profiles) > 0

    @property
    def has_profile(self):
        return len(self.mass_profiles) + len(self.light_profiles) > 0

    @property
    def uses_cluster_inversion(self):
        return type(self.pixelization) is pix.VoronoiBrightnessImage

    def __repr__(self):
        string = "Redshift: {}".format(self.redshift)
        if self.pixelization:
            string += "\nPixelization:\n{}".format(str(self.pixelization))
        if self.regularization:
            string += "\nRegularization:\n{}".format(str(self.regularization))
        if self.hyper_galaxy:
            string += "\nHyper Galaxy:\n{}".format(str(self.hyper_galaxy))
        if self.light_profiles:
            string += "\nLight Profiles:\n{}".format(
                "\n".join(map(str, self.light_profiles))
            )
        if self.mass_profiles:
            string += "\nMass Profiles:\n{}".format(
                "\n".join(map(str, self.mass_profiles))
            )
        return string

    def __eq__(self, other):
        return all(
            (
                isinstance(other, Galaxy),
                self.pixelization == other.pixelization,
                self.redshift == other.redshift,
                self.hyper_galaxy == other.hyper_galaxy,
                self.light_profiles == other.light_profiles,
                self.mass_profiles == other.mass_profiles,
            )
        )

    @reshape_array_from_grid
    def profile_image_from_grid(self, grid, return_in_2d=True, return_binned=True):
        """Calculate the summed image of all of the galaxy's light profiles using a grid of Cartesian (y,x) \
        coordinates.
        
        If the galaxy has no light profiles, a grid of zeros is returned.
        
        See *profiles.light_profiles* for a description of how light profile image are computed.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        return_in_2d : bool
            If *True*, the returned array is mapped to its unmasked 2D shape, if *False* it is the masked 1D shape.
        return_binned : bool
            If *True*, the returned array which is computed on a sub-grid is binned up to the grid dimensions \
            by taking the mean of all sub-gridded values. If *False*, the array is returned on the dimensions of the \
            sub-grid.
        """
        if self.has_light_profile:
            return sum(
                map(
                    lambda p: p.profile_image_from_grid(
                        grid=grid, return_in_2d=False, return_binned=False
                    ),
                    self.light_profiles,
                )
            )
        else:
            return np.zeros((grid.shape[0],))

    @reshape_array_from_grid_and_psf
    def blurred_profile_image_from_grid_and_psf(
        self, grid, psf, preload_blurring_grid=None, return_in_2d=True
    ):

        profile_image = self.profile_image_from_grid(
            grid=grid, return_in_2d=True, return_binned=True
        )

        if preload_blurring_grid is None:
            preload_blurring_grid = grid.blurring_grid_from_psf_shape(
                psf_shape=psf.shape
            )

        blurring_image = self.profile_image_from_grid(
            grid=preload_blurring_grid, return_in_2d=True, return_binned=True
        )

        return psf.convolve(profile_image + blurring_image)

    @reshape_array_from_grid_and_convolver
    def blurred_profile_image_from_grid_and_convolver(
        self, grid, convolver, preload_blurring_grid=None, return_in_2d=True
    ):

        if convolver.blurring_mask is None:
            blurring_mask = grid.mask.blurring_mask_from_psf_shape(
                psf_shape=convolver.psf.shape
            )
            convolver = convolver.convolver_with_blurring_mask_added(
                blurring_mask=blurring_mask
            )

        profile_image = self.profile_image_from_grid(
            grid=grid, return_in_2d=False, return_binned=True
        )

        if preload_blurring_grid is None:
            preload_blurring_grid = grid.blurring_grid_from_psf_shape(
                psf_shape=convolver.psf.shape
            )

        blurring_image = self.profile_image_from_grid(
            grid=preload_blurring_grid, return_in_2d=False, return_binned=True
        )

        return convolver.convolve_image(
            image_array=profile_image, blurring_array=blurring_image
        )

    def visibilities_from_grid_and_transformer(self, grid, transformer):

        profile_image_plane_image_1d = self.profile_image_from_grid(
            grid=grid, return_in_2d=False, return_binned=True
        )

        return transformer.visibilities_from_image_1d(
            image_1d=profile_image_plane_image_1d
        )

    def luminosity_within_circle_in_units(
        self,
        radius: dim.Length,
        unit_luminosity="eps",
        exposure_time=None,
        cosmology=cosmo.Planck15,
        **kwargs
    ):
        """Compute the total luminosity of the galaxy's light profiles within a circle of specified radius.

        See *light_profiles.luminosity_within_circle* for details of how this is performed.

        Parameters
        ----------
        radius : float
            The radius of the circle to compute the dimensionless mass within.
        unit_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float
            The exposure time of the observation, which converts luminosity from electrons per second units to counts.
        """
        if self.has_light_profile:
            return sum(
                map(
                    lambda p: p.luminosity_within_circle_in_units(
                        radius=radius,
                        unit_luminosity=unit_luminosity,
                        redshift_profile=self.redshift,
                        exposure_time=exposure_time,
                        cosmology=cosmology,
                        kwargs=kwargs,
                    ),
                    self.light_profiles,
                )
            )
        return None

    def luminosity_within_ellipse_in_units(
        self,
        major_axis: dim.Length,
        unit_luminosity="eps",
        exposure_time=None,
        cosmology=cosmo.Planck15,
        **kwargs
    ):
        """Compute the total luminosity of the galaxy's light profiles, within an
        ellipse of specified major axis. This is performed via integration of each
        light profile and is centred, oriented and aligned with each light model's
        individual geometry.

        See *light_profiles.luminosity_within_ellipse* for details of how this is \
        performed.

        Parameters
        ----------
        major_axis : float
            The major-axis radius of the ellipse.
        unit_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float
            The exposure time of the observation, which converts luminosity from \
            electrons per second units to counts.
        """
        if self.has_light_profile:
            return sum(
                map(
                    lambda p: p.luminosity_within_ellipse_in_units(
                        major_axis=major_axis,
                        unit_luminosity=unit_luminosity,
                        redshift_profile=self.redshift,
                        exposure_time=exposure_time,
                        cosmology=cosmology,
                        kwargs=kwargs,
                    ),
                    self.light_profiles,
                )
            )
        return None

    @reshape_array_from_grid
    def convergence_from_grid(self, grid, return_in_2d=True, return_binned=True):
        """Compute the summed convergence of the galaxy's mass profiles using a grid \
        of Cartesian (y,x) coordinates.

        If the galaxy has no mass profiles, a grid of zeros is returned.
        
        See *profiles.mass_profiles* module for details of how this is performed.

        The *reshape_returned_array* decorator reshapes the NumPy array the convergence is outputted on. See \
        *grids.reshape_returned_array* for a description of the output.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        return_in_2d : bool
            If *True*, the returned array is mapped to its unmasked 2D shape, if *False* it is the masked 1D shape.
        return_binned : bool
            If *True*, the returned array which is computed on a sub-grid is binned up to the grid dimensions \
            by taking the mean of all sub-gridded values. If *False*, the array is returned on the dimensions of the \
            sub-grid.
        """
        if self.has_mass_profile:
            return sum(
                map(
                    lambda p: p.convergence_from_grid(
                        grid=grid, return_in_2d=False, return_binned=False
                    ),
                    self.mass_profiles,
                )
            )
        return np.zeros((grid.shape[0],))

    @reshape_array_from_grid
    def potential_from_grid(self, grid, return_in_2d=True, return_binned=True):
        """Compute the summed gravitational potential of the galaxy's mass profiles \
        using a grid of Cartesian (y,x) coordinates.

        If the galaxy has no mass profiles, a grid of zeros is returned.

        See *profiles.mass_profiles* module for details of how this is performed.

                The *reshape_returned_array* decorator reshapes the NumPy array the convergence is outputted on. See \
        *grids.reshape_returned_array* for a description of the output.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        return_in_2d : bool
            If *True*, the returned array is mapped to its unmasked 2D shape, if *False* it is the masked 1D shape.
        return_binned : bool
            If *True*, the returned array which is computed on a sub-grid is binned up to the grid dimensions \
            by taking the mean of all sub-gridded values. If *False*, the array is returned on the dimensions of the \
            sub-grid.
        """
        if self.has_mass_profile:
            return sum(
                map(
                    lambda p: p.potential_from_grid(
                        grid=grid, return_in_2d=False, return_binned=False
                    ),
                    self.mass_profiles,
                )
            )
        return np.zeros((grid.shape[0],))

    @reshape_returned_grid
    def deflections_from_grid(self, grid, return_in_2d=True, return_binned=True):
        """Compute the summed (y,x) deflection angles of the galaxy's mass profiles \
        using a grid of Cartesian (y,x) coordinates.

        If the galaxy has no mass profiles, two grid of zeros are returned.

        See *profiles.mass_profiles* module for details of how this is performed.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        """
        if self.has_mass_profile:
            return sum(
                map(
                    lambda p: p.deflections_from_grid(
                        grid=grid, return_in_2d=False, return_binned=False
                    ),
                    self.mass_profiles,
                )
            )
        return np.full((grid.shape[0], 2), 0.0)

    @reshape_returned_grid
    def deflections_via_potential_from_grid(
        self, grid, return_in_2d=True, return_binned=True
    ):
        potential_2d = self.potential_from_grid(
            grid=grid, return_in_2d=True, return_binned=False
        )

        deflections_y_2d = np.gradient(potential_2d, grid.in_2d[:, 0, 0], axis=0)
        deflections_x_2d = np.gradient(potential_2d, grid.in_2d[0, :, 1], axis=1)

        return np.stack((deflections_y_2d, deflections_x_2d), axis=-1)

    @reshape_array_from_grid
    def lensing_jacobian_a11_from_grid(
        self, grid, return_in_2d=True, return_binned=True
    ):

        deflections_2d = self.deflections_from_grid(
            grid=grid, return_in_2d=True, return_binned=False
        )

        return 1.0 - np.gradient(deflections_2d[:, :, 1], grid.in_2d[0, :, 1], axis=1)

    @reshape_array_from_grid
    def lensing_jacobian_a12_from_grid(
        self, grid, return_in_2d=True, return_binned=True
    ):

        deflections_2d = self.deflections_from_grid(
            grid=grid, return_in_2d=True, return_binned=False
        )

        return -1.0 * np.gradient(deflections_2d[:, :, 1], grid.in_2d[:, 0, 0], axis=0)

    @reshape_array_from_grid
    def lensing_jacobian_a21_from_grid(
        self, grid, return_in_2d=True, return_binned=True
    ):

        deflections_2d = self.deflections_from_grid(
            grid=grid, return_in_2d=True, return_binned=False
        )

        return -1.0 * np.gradient(deflections_2d[:, :, 0], grid.in_2d[0, :, 1], axis=1)

    @reshape_array_from_grid
    def lensing_jacobian_a22_from_grid(
        self, grid, return_in_2d=True, return_binned=True
    ):

        deflections_2d = self.deflections_from_grid(
            grid=grid, return_in_2d=True, return_binned=False
        )

        return 1 - np.gradient(deflections_2d[:, :, 0], grid.in_2d[:, 0, 0], axis=0)

    def lensing_jacobian_from_grid(self, grid, return_in_2d=True, return_binned=True):

        a11 = self.lensing_jacobian_a11_from_grid(
            grid=grid, return_in_2d=return_in_2d, return_binned=return_binned
        )

        a12 = self.lensing_jacobian_a12_from_grid(
            grid=grid, return_in_2d=return_in_2d, return_binned=return_binned
        )

        a21 = self.lensing_jacobian_a21_from_grid(
            grid=grid, return_in_2d=return_in_2d, return_binned=return_binned
        )

        a22 = self.lensing_jacobian_a22_from_grid(
            grid=grid, return_in_2d=return_in_2d, return_binned=return_binned
        )

        return np.array([[a11, a12], [a21, a22]])

    @reshape_array_from_grid
    def convergence_via_jacobian_from_grid(
        self, grid, return_in_2d=True, return_binned=True
    ):

        jacobian = self.lensing_jacobian_from_grid(
            grid=grid, return_in_2d=False, return_binned=False
        )

        convergence = 1 - 0.5 * (jacobian[0, 0] + jacobian[1, 1])

        return convergence

    @reshape_array_from_grid
    def shear_via_jacobian_from_grid(self, grid, return_in_2d=True, return_binned=True):

        jacobian = self.lensing_jacobian_from_grid(
            grid=grid, return_in_2d=True, return_binned=False
        )

        gamma_1 = 0.5 * (jacobian[1, 1] - jacobian[0, 0])
        gamma_2 = -0.5 * (jacobian[0, 1] + jacobian[1, 0])

        return (gamma_1 ** 2 + gamma_2 ** 2) ** 0.5

    @reshape_array_from_grid
    def tangential_eigen_value_from_grid(
        self, grid, return_in_2d=True, return_binned=True
    ):

        convergence = self.convergence_via_jacobian_from_grid(
            grid=grid, return_in_2d=False, return_binned=False
        )

        shear = self.shear_via_jacobian_from_grid(
            grid=grid, return_in_2d=False, return_binned=False
        )

        return 1 - convergence - shear

    @reshape_array_from_grid
    def radial_eigen_value_from_grid(self, grid, return_in_2d=True, return_binned=True):

        convergence = self.convergence_via_jacobian_from_grid(
            grid=grid, return_in_2d=False, return_binned=False
        )

        shear = self.shear_via_jacobian_from_grid(
            grid=grid, return_in_2d=False, return_binned=False
        )

        return 1 - convergence + shear

    @reshape_array_from_grid
    def magnification_from_grid(self, grid, return_in_2d=True, return_binned=True):

        jacobian = self.lensing_jacobian_from_grid(
            grid=grid, return_in_2d=False, return_binned=False
        )

        det_jacobian = jacobian[0, 0] * jacobian[1, 1] - jacobian[0, 1] * jacobian[1, 0]

        return 1 / det_jacobian

    def tangential_critical_curve_from_grid(self, grid):

        lambda_tangential_2d = self.tangential_eigen_value_from_grid(
            grid=grid, return_in_2d=True, return_binned=False
        )

        tangential_critical_curve_indices = measure.find_contours(
            lambda_tangential_2d, 0
        )

        if tangential_critical_curve_indices == []:
            return []

        return grid.marching_squares_grid_pixels_to_grid_arcsec(
            grid_pixels=tangential_critical_curve_indices[0],
            shape=lambda_tangential_2d.shape,
        )

    def radial_critical_curve_from_grid(self, grid):

        lambda_radial_2d = self.radial_eigen_value_from_grid(
            grid=grid, return_in_2d=True, return_binned=False
        )

        radial_critical_curve_indices = measure.find_contours(lambda_radial_2d, 0)

        if radial_critical_curve_indices == []:
            return []

        return grid.marching_squares_grid_pixels_to_grid_arcsec(
            grid_pixels=radial_critical_curve_indices[0], shape=lambda_radial_2d.shape
        )

    def tangential_caustic_from_grid(self, grid):

        tangential_critical_curve = self.tangential_critical_curve_from_grid(grid=grid)

        if tangential_critical_curve == []:
            return []

        deflections_1d = self.deflections_from_grid(
            grid=tangential_critical_curve, return_in_2d=False, return_binned=False
        )

        return tangential_critical_curve - deflections_1d

    def radial_caustic_from_grid(self, grid):

        radial_critical_curve = self.radial_critical_curve_from_grid(grid=grid)

        if radial_critical_curve == []:
            return []

        deflections_1d = self.deflections_from_grid(
            grid=radial_critical_curve, return_in_2d=False, return_binned=False
        )

        return radial_critical_curve - deflections_1d

    def critical_curves_from_grid(self, grid):
        return [
            self.tangential_critical_curve_from_grid(grid=grid),
            self.radial_critical_curve_from_grid(grid=grid),
        ]

    def caustics_from_grid(self, grid):
        return [
            self.tangential_caustic_from_grid(grid=grid),
            self.radial_caustic_from_grid(grid=grid),
        ]

    def mass_within_circle_in_units(
        self,
        radius: dim.Length,
        redshift_source=None,
        unit_mass="solMass",
        cosmology=cosmo.Planck15,
        **kwargs
    ):
        """Compute the total angular mass of the galaxy's mass profiles within a \
        circle of specified radius.

        See *profiles.mass_profiles.mass_within_circle* for details of how this is \
        performed.

        Parameters
        ----------
        radius : float
            The radius of the circle to compute the dimensionless mass within.
        unit_mass : str
            The units the mass is returned in (angular | solMass).
        """
        if self.has_mass_profile:
            return sum(
                map(
                    lambda p: p.mass_within_circle_in_units(
                        radius=radius,
                        redshift_profile=self.redshift,
                        redshift_source=redshift_source,
                        unit_mass=unit_mass,
                        cosmology=cosmology,
                        kwargs=kwargs,
                    ),
                    self.mass_profiles,
                )
            )
        return None

    def mass_within_ellipse_in_units(
        self,
        major_axis: dim.Length,
        redshift_source=None,
        unit_mass="solMass",
        cosmology=cosmo.Planck15,
        **kwargs
    ):
        """Compute the total angular mass of the galaxy's mass profiles within an \
        ellipse of specified major_axis.

        See *profiles.mass_profiles.angualr_mass_within_ellipse* for details of how \
        this is performed.

        Parameters
        ----------
        major_axis : float
            The major-axis radius of the ellipse.
        """
        if self.has_mass_profile:
            return sum(
                map(
                    lambda p: p.mass_within_ellipse_in_units(
                        major_axis=major_axis,
                        redshift_profile=self.redshift,
                        redshift_source=redshift_source,
                        unit_mass=unit_mass,
                        cosmology=cosmology,
                        kwargs=kwargs,
                    ),
                    self.mass_profiles,
                )
            )
        return None

    def einstein_radius_in_units(
        self, unit_length="arcsec", cosmology=cosmo.Planck15, **kwargs
    ):
        """The Einstein Radius of this galaxy, which is the sum of Einstein Radii of \
        its mass profiles.

        If the galaxy is composed of multiple elliptical profiles with different \
        axis-ratios, this Einstein Radius may be inaccurate. This is because the \
        differently oriented ellipses of each mass profile """

        if self.has_mass_profile:
            return sum(
                map(
                    lambda p: p.einstein_radius_in_units(
                        unit_length=unit_length,
                        redshift_profile=self.redshift,
                        cosmology=cosmology,
                    ),
                    self.mass_profiles,
                )
            )
        return None

    def einstein_mass_in_units(
        self,
        unit_mass="solMass",
        redshift_source=None,
        cosmology=cosmo.Planck15,
        **kwargs
    ):
        """The Einstein Mass of this galaxy, which is the sum of Einstein Radii of its
        mass profiles.

        If the galaxy is composed of multiple ellipitcal profiles with different \
        axis-ratios, this Einstein Mass may be inaccurate. This is because the \
        differently oriented ellipses of each mass profile """

        if self.has_mass_profile:
            return sum(
                map(
                    lambda p: p.einstein_mass_in_units(
                        unit_mass=unit_mass,
                        redshift_profile=self.redshift,
                        redshift_source=redshift_source,
                        cosmology=cosmology,
                        kwargs=kwargs,
                    ),
                    self.mass_profiles,
                )
            )
        return None

    def summarize_in_units(
        self,
        radii,
        whitespace=80,
        unit_length="arcsec",
        unit_luminosity="eps",
        unit_mass="solMass",
        redshift_source=None,
        cosmology=cosmo.Planck15,
        **kwargs
    ):

        if hasattr(self, "name"):
            summary = ["Galaxy = {}\n".format(self.name)]
            prefix_galaxy = self.name + "_"
        else:
            summary = ["Galaxy\n"]
            prefix_galaxy = ""

        summary += [
            af.text_util.label_and_value_string(
                label=prefix_galaxy + "redshift",
                value=self.redshift,
                whitespace=whitespace,
            )
        ]

        if self.has_light_profile:
            summary += self.summarize_light_profiles_in_units(
                whitespace=whitespace,
                prefix=prefix_galaxy,
                radii=radii,
                unit_length=unit_length,
                unit_luminosity=unit_luminosity,
                redshift_source=redshift_source,
                cosmology=cosmology,
                kwargs=kwargs,
            )

        if self.has_mass_profile:
            summary += self.summarize_mass_profiles_in_units(
                whitespace=whitespace,
                prefix=prefix_galaxy,
                radii=radii,
                unit_length=unit_length,
                unit_mass=unit_mass,
                redshift_source=redshift_source,
                cosmology=cosmology,
                kwargs=kwargs,
            )

        return summary

    def summarize_light_profiles_in_units(
        self,
        radii,
        whitespace=80,
        prefix="",
        unit_length="arcsec",
        unit_luminosity="eps",
        redshift_source=None,
        cosmology=cosmo.Planck15,
        **kwargs
    ):

        summary = ["\nGALAXY LIGHT\n\n"]

        for radius in radii:
            luminosity = self.luminosity_within_circle_in_units(
                unit_luminosity=unit_luminosity,
                radius=radius,
                redshift_source=redshift_source,
                cosmology=cosmology,
                kwargs=kwargs,
            )

            summary += [
                text_util.within_radius_label_value_and_unit_string(
                    prefix=prefix + "luminosity",
                    radius=radius,
                    unit_length=unit_length,
                    value=luminosity,
                    unit_value=unit_luminosity,
                    whitespace=whitespace,
                )
            ]

        summary.append("\nLIGHT PROFILES:\n\n")

        for light_profile in self.light_profiles:
            summary += light_profile.summarize_in_units(
                radii=radii,
                whitespace=whitespace,
                unit_length=unit_length,
                unit_luminosity=unit_luminosity,
                redshift_profile=self.redshift,
                redshift_source=redshift_source,
                cosmology=cosmology,
                kwargs=kwargs,
            )

            summary += "\n"

        return summary

    def summarize_mass_profiles_in_units(
        self,
        radii,
        whitespace=80,
        prefix="",
        unit_length="arcsec",
        unit_mass="solMass",
        redshift_source=None,
        cosmology=cosmo.Planck15,
        **kwargs
    ):

        summary = ["\nGALAXY MASS\n\n"]

        einstein_radius = self.einstein_radius_in_units(
            unit_length=unit_length, cosmology=cosmology
        )

        summary += [
            af.text_util.label_value_and_unit_string(
                label=prefix + "einstein_radius",
                value=einstein_radius,
                unit=unit_length,
                whitespace=whitespace,
            )
        ]

        einstein_mass = self.einstein_mass_in_units(
            unit_mass=unit_mass,
            redshift_source=redshift_source,
            cosmology=cosmology,
            kwargs=kwargs,
        )

        summary += [
            af.text_util.label_value_and_unit_string(
                label=prefix + "einstein_mass",
                value=einstein_mass,
                unit=unit_mass,
                whitespace=whitespace,
            )
        ]

        for radius in radii:
            mass = self.mass_within_circle_in_units(
                unit_mass=unit_mass,
                radius=radius,
                redshift_source=redshift_source,
                cosmology=cosmology,
                kwargs=kwargs,
            )

            summary += [
                text_util.within_radius_label_value_and_unit_string(
                    prefix=prefix + "mass",
                    radius=radius,
                    unit_length=unit_length,
                    value=mass,
                    unit_value=unit_mass,
                    whitespace=whitespace,
                )
            ]

        summary += ["\nMASS PROFILES:\n\n"]

        for mass_profile in self.mass_profiles:
            summary += mass_profile.summarize_in_units(
                radii=radii,
                whitespace=whitespace,
                unit_length=unit_length,
                unit_mass=unit_mass,
                redshift_profile=self.redshift,
                redshift_source=redshift_source,
                cosmology=cosmology,
                kwargs=kwargs,
            )

            summary += "\n"

        return summary


class HyperGalaxy(object):
    _ids = count()

    def __init__(self, contribution_factor=0.0, noise_factor=0.0, noise_power=1.0):
        """ If a *Galaxy* is given a *HyperGalaxy* as an attribute, the noise-map in \
        the regions of the image that the galaxy is located will be hyper, to prevent \
        over-fitting of the galaxy.
        
        This is performed by first computing the hyper_galaxies-galaxy's 'contribution-map', \
        which determines the fraction of flux in every pixel of the image that can be \
        associated with this particular hyper_galaxies-galaxy. This is computed using \
        hyper_galaxies-hyper_galaxies set (e.g. fitting.fit_data.FitDataHyper), which includes  best-fit \
        unblurred_image_1d of the galaxy's light from a previous analysis phase.
         
        The *HyperGalaxy* class contains the hyper_galaxies-parameters which are associated \
        with this galaxy for scaling the noise-map.
        
        Parameters
        -----------
        contribution_factor : float
            Factor that adjusts how much of the galaxy's light is attributed to the
            contribution map.
        noise_factor : float
            Factor by which the noise-map is increased in the regions of the galaxy's
            contribution map.
        noise_power : float
            The power to which the contribution map is raised when scaling the
            noise-map.
        """
        self.contribution_factor = contribution_factor
        self.noise_factor = noise_factor
        self.noise_power = noise_power

        self.component_number = next(self._ids)

    def hyper_noise_map_from_hyper_images_and_noise_map(
        self, hyper_model_image, hyper_galaxy_image, noise_map
    ):
        contribution_map = self.contribution_map_from_hyper_images(
            hyper_model_image=hyper_model_image, hyper_galaxy_image=hyper_galaxy_image
        )
        return self.hyper_noise_map_from_contribution_map(
            noise_map=noise_map, contribution_map=contribution_map
        )

    def contribution_map_from_hyper_images(self, hyper_model_image, hyper_galaxy_image):
        """Compute the contribution map of a galaxy, which represents the fraction of
        flux in each pixel that the galaxy is attributed to contain, hyper to the
        *contribution_factor* hyper_galaxies-parameter.

        This is computed by dividing that galaxy's flux by the total flux in that \
        pixel and then scaling by the maximum flux such that the contribution map \
        ranges between 0 and 1.

        Parameters
        -----------
        hyper_model_image : ndarray
            The best-fit model image to the observed image from a previous analysis
            phase. This provides the total light attributed to each image pixel by the
            model.
        hyper_galaxy_image : ndarray
            A model image of the galaxy (from light profiles or an inversion) from a
            previous analysis phase.
        """
        contribution_map = np.divide(
            hyper_galaxy_image, np.add(hyper_model_image, self.contribution_factor)
        )
        contribution_map = np.divide(contribution_map, np.max(contribution_map))
        return contribution_map

    def hyper_noise_map_from_contribution_map(self, noise_map, contribution_map):
        """Compute a hyper galaxy hyper_galaxies noise-map from a baseline noise-map.

        This uses the galaxy contribution map and the *noise_factor* and *noise_power*
        hyper_galaxies-parameters.

        Parameters
        -----------
        noise_map : ndarray
            The observed noise-map (before scaling).
        contribution_map : ndarray
            The galaxy contribution map.
        """
        return self.noise_factor * (noise_map * contribution_map) ** self.noise_power

    def __eq__(self, other):
        if isinstance(other, HyperGalaxy):
            return (
                self.contribution_factor == other.contribution_factor
                and self.noise_factor == other.noise_factor
                and self.noise_power == other.noise_power
            )
        return False

    def __str__(self):
        return "\n".join(["{}: {}".format(k, v) for k, v in self.__dict__.items()])


class Redshift(float):
    def __new__(cls, redshift):
        # noinspection PyArgumentList
        return float.__new__(cls, redshift)

    def __init__(self, redshift):
        float.__init__(redshift)
