from astropy import cosmology as cosmo

import autofit as af

from autolens.model.galaxy import galaxy_fit, galaxy_data as gd
from autolens.model.galaxy.plotters import galaxy_fit_plotters
from autolens.pipeline.phase.phase import Phase

class PhaseGalaxy(af.AbstractPhase):
    galaxies = af.PhaseProperty("galaxies")

    def __init__(
        self,
        phase_name,
        phase_folders=tuple(),
        galaxies=None,
        use_image=False,
        use_convergence=False,
        use_potential=False,
        use_deflections=False,
        optimizer_class=af.MultiNest,
        sub_size=2,
        pixel_scale_interpolation_grid=None,
        mask_function=None,
        cosmology=cosmo.Planck15,
    ):
        """
        A phase in an lens pipeline. Uses the set non_linear optimizer to try to fit
        models and hyper_galaxies passed to it.

        Parameters
        ----------
        optimizer_class: class
            The class of a non_linear optimizer
        sub_size: int
            The side length of the subgrid
        """

        super(PhaseGalaxy, self).__init__(
            phase_name=phase_name,
            phase_folders=phase_folders,
            optimizer_class=optimizer_class,
            cosmology=cosmology,
        )
        self.use_image = use_image
        self.use_convergence = use_convergence
        self.use_potential = use_potential
        self.use_deflections = use_deflections
        self.galaxies = galaxies
        self.sub_size = sub_size
        self.pixel_scale_interpolation_grid = pixel_scale_interpolation_grid
        self.mask_function = mask_function

    def run(self, galaxy_data, results=None, mask=None):
        """
        Run this phase.

        Parameters
        ----------
        galaxy_data
        mask: Mask
            The default masks passed in by the pipeline
        results: autofit.tools.pipeline.ResultsCollection
            An object describing the results of the last phase or None if no phase has
            been executed

        Returns
        -------
        result: AbstractPhase.Result
            A result object comprising the best fit model and other hyper_galaxies.
        """
        analysis = self.make_analysis(
            galaxy_data=galaxy_data, results=results, mask=mask
        )

        self.variable = self.variable.populate(results)
        self.customize_priors(results)
        self.assert_and_save_pickle()

        result = self.run_analysis(analysis)

        return self.make_result(result, analysis)

    def make_analysis(self, galaxy_data, results=None, mask=None):
        """
        Create an lens object. Also calls the prior passing and lens_data modifying
        functions to allow child classes to change the behaviour of the phase.

        Parameters
        ----------
        galaxy_data
        mask: Mask
            The default masks passed in by the pipeline
        results: autofit.tools.pipeline.ResultsCollection
            The result from the previous phase

        Returns
        -------
        lens: Analysis
            An lens object that the non-linear optimizer calls to determine the fit of a
             set of values
        """

        mask = setup_phase_mask(
            data=galaxy_data[0],
            mask=mask,
            mask_function=self.mask_function,
            inner_mask_radii=None,
        )

        if self.use_image or self.use_convergence or self.use_potential:

            galaxy_data = gd.GalaxyFitData(
                galaxy_data=galaxy_data[0],
                mask=mask,
                sub_size=self.sub_size,
                pixel_scale_interpolation_grid=self.pixel_scale_interpolation_grid,
                use_image=self.use_image,
                use_convergence=self.use_convergence,
                use_potential=self.use_potential,
                use_deflections_y=self.use_deflections,
                use_deflections_x=self.use_deflections,
            )

            return self.AnalysisSingle(
                galaxy_data=galaxy_data, cosmology=self.cosmology, results=results
            )

        elif self.use_deflections:

            galaxy_data_y = gd.GalaxyFitData(
                galaxy_data=galaxy_data[0],
                mask=mask,
                sub_size=self.sub_size,
                pixel_scale_interpolation_grid=self.pixel_scale_interpolation_grid,
                use_image=self.use_image,
                use_convergence=self.use_convergence,
                use_potential=self.use_potential,
                use_deflections_y=self.use_deflections,
                use_deflections_x=False,
            )

            galaxy_data_x = gd.GalaxyFitData(
                galaxy_data=galaxy_data[1],
                mask=mask,
                sub_size=self.sub_size,
                pixel_scale_interpolation_grid=self.pixel_scale_interpolation_grid,
                use_image=self.use_image,
                use_convergence=self.use_convergence,
                use_potential=self.use_potential,
                use_deflections_y=False,
                use_deflections_x=self.use_deflections,
            )

            return self.AnalysisDeflections(
                galaxy_data_y=galaxy_data_y,
                galaxy_data_x=galaxy_data_x,
                cosmology=self.cosmology,
                results=results,
            )

    # noinspection PyAbstractClass
    class Analysis(Phase.Analysis):
        def __init__(self, cosmology, results):
            super(PhaseGalaxy.Analysis, self).__init__(
                cosmology=cosmology, results=results
            )

            self.plot_galaxy_fit_all_at_end_png = af.conf.instance.visualize.get(
                "plots", "plot_galaxy_fit_all_at_end_png", bool
            )
            self.plot_galaxy_fit_all_at_end_fits = af.conf.instance.visualize.get(
                "plots", "plot_galaxy_fit_all_at_end_fits", bool
            )
            self.plot_galaxy_fit_as_subplot = af.conf.instance.visualize.get(
                "plots", "plot_galaxy_fit_as_subplot", bool
            )
            self.plot_galaxy_fit_image = af.conf.instance.visualize.get(
                "plots", "plot_galaxy_fit_image", bool
            )
            self.plot_galaxy_fit_noise_map = af.conf.instance.visualize.get(
                "plots", "plot_galaxy_fit_noise_map", bool
            )
            self.plot_galaxy_fit_model_image = af.conf.instance.visualize.get(
                "plots", "plot_galaxy_fit_model_image", bool
            )
            self.plot_galaxy_fit_residual_map = af.conf.instance.visualize.get(
                "plots", "plot_galaxy_fit_residual_map", bool
            )
            self.plot_galaxy_fit_chi_squared_map = af.conf.instance.visualize.get(
                "plots", "plot_galaxy_fit_chi_squared_map", bool
            )

        @classmethod
        def describe(cls, instance):
            return "\nRunning galaxy fit for... \n\nGalaxies::\n{}\n\n".format(
                instance.galaxies
            )

    # noinspection PyAbstractClass
    class AnalysisSingle(Analysis):
        def __init__(self, galaxy_data, cosmology, results=None):
            super(PhaseGalaxy.AnalysisSingle, self).__init__(
                cosmology=cosmology, results=results
            )

            self.galaxy_data = galaxy_data

        def fit(self, instance):
            fit = self.fit_for_instance(instance=instance)
            return fit.figure_of_merit

        def visualize(self, instance, image_path, during_analysis):

            self.plot_count += 1
            fit = self.fit_for_instance(instance=instance)

            if self.plot_galaxy_fit_as_subplot:
                galaxy_fit_plotters.plot_fit_subplot(
                    fit=fit,
                    should_plot_mask=self.should_plot_mask,
                    zoom_around_mask=self.zoom_around_mask,
                    units=self.plot_units,
                    output_path=image_path,
                    output_format="png",
                )

            if during_analysis:

                galaxy_fit_plotters.plot_fit_individuals(
                    fit=fit,
                    should_plot_mask=self.should_plot_mask,
                    zoom_around_mask=self.zoom_around_mask,
                    should_plot_image=self.plot_galaxy_fit_image,
                    should_plot_noise_map=self.plot_galaxy_fit_noise_map,
                    should_plot_model_image=self.plot_galaxy_fit_model_image,
                    should_plot_residual_map=self.plot_galaxy_fit_residual_map,
                    should_plot_chi_squared_map=self.plot_galaxy_fit_chi_squared_map,
                    units=self.plot_units,
                    output_path=image_path,
                    output_format="png",
                )

            elif not during_analysis:

                if self.plot_ray_tracing_all_at_end_png:
                    galaxy_fit_plotters.plot_fit_individuals(
                        fit=fit,
                        should_plot_mask=self.should_plot_mask,
                        zoom_around_mask=self.zoom_around_mask,
                        should_plot_image=True,
                        should_plot_noise_map=True,
                        should_plot_model_image=True,
                        should_plot_residual_map=True,
                        should_plot_chi_squared_map=True,
                        units=self.plot_units,
                        output_path=image_path,
                        output_format="png",
                    )

                if self.plot_ray_tracing_all_at_end_fits:
                    galaxy_fit_plotters.plot_fit_individuals(
                        fit=fit,
                        should_plot_mask=self.should_plot_mask,
                        zoom_around_mask=self.zoom_around_mask,
                        should_plot_image=True,
                        should_plot_noise_map=True,
                        should_plot_model_image=True,
                        should_plot_residual_map=True,
                        should_plot_chi_squared_map=True,
                        units=self.plot_units,
                        output_path="{}/fits/".format(image_path),
                        output_format="fits",
                    )

            return fit

        def fit_for_instance(self, instance):
            """
            Determine the fit of a lens galaxy and source galaxy to the lens_data in
            this lens.

            Parameters
            ----------
            instance
                A model instance with attributes

            Returns
            -------
            fit: Fit
                A fractional value indicating how well this model fit and the model
                lens_data itself
            """
            return galaxy_fit.GalaxyFit(
                galaxy_data=self.galaxy_data, model_galaxies=instance.galaxies
            )

    # noinspection PyAbstractClass
    class AnalysisDeflections(Analysis):
        def __init__(self, galaxy_data_y, galaxy_data_x, cosmology, results=None):
            super(PhaseGalaxy.AnalysisDeflections, self).__init__(
                cosmology=cosmology, results=results
            )

            self.galaxy_data_y = galaxy_data_y
            self.galaxy_data_x = galaxy_data_x

        def fit(self, instance):
            fit_y, fit_x = self.fit_for_instance(instance=instance)
            return fit_y.figure_of_merit + fit_x.figure_of_merit

        def visualize(self, instance, image_path, during_analysis):

            output_image_y_path = "{}/fit_y_".format(image_path)
            output_fits_y_path = "{}/fits/fit_y".format(image_path)
            output_image_x_path = "{}/fit_x_".format(image_path)
            output_fits_x_path = "{}/fits/fit_x".format(image_path)

            self.plot_count += 1
            fit_y, fit_x = self.fit_for_instance(instance=instance)

            if self.plot_galaxy_fit_as_subplot:
                galaxy_fit_plotters.plot_fit_subplot(
                    fit=fit_y,
                    should_plot_mask=self.should_plot_mask,
                    zoom_around_mask=self.zoom_around_mask,
                    units=self.plot_units,
                    output_path=output_image_y_path,
                    output_format="png",
                )

                galaxy_fit_plotters.plot_fit_subplot(
                    fit=fit_x,
                    should_plot_mask=self.should_plot_mask,
                    zoom_around_mask=self.zoom_around_mask,
                    units=self.plot_units,
                    output_path=output_image_x_path,
                    output_format="png",
                )

            if during_analysis:

                galaxy_fit_plotters.plot_fit_individuals(
                    fit=fit_y,
                    should_plot_mask=self.should_plot_mask,
                    zoom_around_mask=self.zoom_around_mask,
                    should_plot_image=self.plot_galaxy_fit_image,
                    should_plot_noise_map=self.plot_galaxy_fit_noise_map,
                    should_plot_model_image=self.plot_galaxy_fit_model_image,
                    should_plot_residual_map=self.plot_galaxy_fit_residual_map,
                    should_plot_chi_squared_map=self.plot_galaxy_fit_chi_squared_map,
                    units=self.plot_units,
                    output_path=output_image_y_path,
                    output_format="png",
                )

                galaxy_fit_plotters.plot_fit_individuals(
                    fit=fit_x,
                    should_plot_mask=self.should_plot_mask,
                    zoom_around_mask=self.zoom_around_mask,
                    should_plot_image=self.plot_galaxy_fit_image,
                    should_plot_noise_map=self.plot_galaxy_fit_noise_map,
                    should_plot_model_image=self.plot_galaxy_fit_model_image,
                    should_plot_residual_map=self.plot_galaxy_fit_residual_map,
                    should_plot_chi_squared_map=self.plot_galaxy_fit_chi_squared_map,
                    units=self.plot_units,
                    output_path=output_image_x_path,
                    output_format="png",
                )

            elif not during_analysis:

                if self.plot_ray_tracing_all_at_end_png:
                    galaxy_fit_plotters.plot_fit_individuals(
                        fit=fit_y,
                        should_plot_mask=self.should_plot_mask,
                        zoom_around_mask=self.zoom_around_mask,
                        should_plot_image=True,
                        should_plot_noise_map=True,
                        should_plot_model_image=True,
                        should_plot_residual_map=True,
                        should_plot_chi_squared_map=True,
                        units=self.plot_units,
                        output_path=output_image_y_path,
                        output_format="png",
                    )

                    galaxy_fit_plotters.plot_fit_individuals(
                        fit=fit_x,
                        should_plot_mask=self.should_plot_mask,
                        zoom_around_mask=self.zoom_around_mask,
                        should_plot_image=True,
                        should_plot_noise_map=True,
                        should_plot_model_image=True,
                        should_plot_residual_map=True,
                        should_plot_chi_squared_map=True,
                        units=self.plot_units,
                        output_path=output_image_x_path,
                        output_format="png",
                    )

                if self.plot_ray_tracing_all_at_end_fits:
                    galaxy_fit_plotters.plot_fit_individuals(
                        fit=fit_y,
                        should_plot_mask=self.should_plot_mask,
                        zoom_around_mask=self.zoom_around_mask,
                        should_plot_image=True,
                        should_plot_noise_map=True,
                        should_plot_model_image=True,
                        should_plot_residual_map=True,
                        should_plot_chi_squared_map=True,
                        units=self.plot_units,
                        output_path=output_fits_y_path,
                        output_format="fits",
                    )

                    galaxy_fit_plotters.plot_fit_individuals(
                        fit=fit_x,
                        should_plot_mask=self.should_plot_mask,
                        zoom_around_mask=self.zoom_around_mask,
                        should_plot_image=True,
                        should_plot_noise_map=True,
                        should_plot_model_image=True,
                        should_plot_residual_map=True,
                        should_plot_chi_squared_map=True,
                        units=self.plot_units,
                        output_path=output_fits_x_path,
                        output_format="fits",
                    )

            return fit_y, fit_x

        def fit_for_instance(self, instance):

            fit_y = galaxy_fit.GalaxyFit(
                galaxy_data=self.galaxy_data_y, model_galaxies=instance.galaxies
            )
            fit_x = galaxy_fit.GalaxyFit(
                galaxy_data=self.galaxy_data_x, model_galaxies=instance.galaxies
            )

            return fit_y, fit_x
