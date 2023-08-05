from autolens.model.profiles import light_profiles as lp
from autolens.model.profiles import mass_profiles as mp
from autolens.model.galaxy import galaxy
from autolens.lens import ray_tracing
from autolens.array import grids
from autolens.lens.plotters import ray_tracing_plotters

# In this example, we'll use the 'ray-tracing' module, to setup the same lens-plane + source-plane strong
# lens configuration as the previous tutorial, but with a lot less lines of code!

# Let use the same grid we've all grown to know and love by now!
image_plane_grid = grids.Grid.from_shape_pixel_scale_and_sub_grid_size(
    shape=(100, 100), pixel_scale=0.1, sub_grid_size=2
)

# subhalo_0 = galaxy.Galaxy(mass=al.mass_profiles.SphericalNFW(centre=(-1.0, -1.0), kappa_s=1.0, scale_radius=0.5), redshift=0.5)
# subhalo_1 = galaxy.Galaxy(mass=al.mass_profiles.SphericalNFW(centre=(1.0, 1.0), kappa_s=1.0, scale_radius=0.5), redshift=0.4)

lens_galaxy = galaxy.Galaxy(
    mass=al.mass_profiles.EllipticalIsothermal(
        centre=(3.0, 3.0), axis_ratio=0.8, phi=45.0, einstein_radius=1.0
    ),
    redshift=0.5,
)

sheet_galaxy = galaxy.Galaxy(
    sheet=al.mass_profiles.MassSheet(centre=(0.0, 0.0), kappa=0.0), redshift=0.2
)

source_galaxy = galaxy.Galaxy(
    light=al.light_profiles.SphericalSersic(
        centre=(0.0, 0.0), intensity=1.0, effective_radius=1.0, sersic_index=3.0
    ),
    redshift=1.0,
)

tracer = ray_tracing.Tracer.from_galaxies(
    galaxies=[lens_galaxy, sheet_galaxy, source_galaxy],
    image_plane_grid=image_plane_grid,
)

ray_tracing_plotters.plot_ray_tracing_subplot(tracer=tracer)

tracer = ray_tracing.TracerMultiPlanesSliced(
    galaxies=[lens_galaxy],
    line_of_sight_galaxies=[sheet_galaxy],
    galaxies=[source_galaxy],
    planes_between_lenses=[2, 2],
    image_plane_grid=image_plane_grid,
)

ray_tracing_plotters.plot_ray_tracing_subplot(tracer=tracer)
