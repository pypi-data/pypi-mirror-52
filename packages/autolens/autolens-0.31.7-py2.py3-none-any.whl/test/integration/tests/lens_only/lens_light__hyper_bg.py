import autofit as af
import autolens as al
from test.integration.tests import runner

test_type = "lens_only"
test_name = "lens_light__hyper_bg"
data_type = "lens_bulge_disk"
data_resolution = "LSST"


def make_pipeline(name, phase_folders, optimizer_class=af.MultiNest):

    phase1 = al.PhaseImaging(
        phase_name="phase_1",
        phase_folders=phase_folders,
        galaxies=dict(
            lens=al.GalaxyModel(redshift=0.5, light=al.light_profiles.EllipticalSersic)
        ),
        optimizer_class=optimizer_class,
    )

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 40
    phase1.optimizer.sampling_efficiency = 0.8

    phase1 = phase1.extend_with_multiple_hyper_phases(
        hyper_galaxy=True, include_background_sky=True, include_background_noise=True
    )

    class HyperLensPlanePhase(al.PhaseImaging):
        def customize_priors(self, results):

            self.galaxies = results.from_phase("phase_1").variable.galaxies

            self.galaxies.lens.hyper_galaxy = (
                results.last.hyper_combined.constant.galaxies.lens.hyper_galaxy
            )

            self.hyper_image_sky = results.last.hyper_combined.constant.hyper_image_sky

            self.hyper_background_noise = (
                results.last.hyper_combined.constant.hyper_background_noise
            )

    phase2 = HyperLensPlanePhase(
        phase_name="phase_2",
        phase_folders=phase_folders,
        galaxies=dict(
            lens=al.GalaxyModel(
                redshift=0.5,
                light=phase1.result.variable.galaxies.lens.light,
                hyper_galaxy=al.HyperGalaxy,
            )
        ),
        optimizer_class=optimizer_class,
    )

    phase2.optimizer.const_efficiency_mode = True
    phase2.optimizer.n_live_points = 40
    phase2.optimizer.sampling_efficiency = 0.8

    return al.PipelineImaging(name, phase1, phase2)


if __name__ == "__main__":
    import sys

    runner.run(sys.modules[__name__])
