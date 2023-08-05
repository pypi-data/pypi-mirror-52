from autolens.plotters import array_plotters
from autolens import exc


def plot_image(
    fit,
    mask=None,
    extract_array_from_mask=False,
    zoom_around_mask=False,
    positions=None,
    grid=None,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Fit Image",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    grid_pointsize=1,
    mask_pointsize=10,
    position_pointsize=10,
    output_path=None,
    output_format="show",
    output_filename="fit_image",
):
    """Plot the image of a lens fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    image : datas.ccd.datas.CCD
        The datas-datas, which includes the observed datas, noise_map-map, PSF, signal-to-noise_map-map, etc.
    plot_origin : True
        If true, the origin of the datas's coordinate system is plotted as a 'x'.
    """

    image = fit.image(return_in_2d=True)

    array_plotters.plot_array(
        array=image,
        grid=grid,
        mask=mask,
        extract_array_from_mask=extract_array_from_mask,
        zoom_around_mask=zoom_around_mask,
        positions=positions,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        grid_pointsize=grid_pointsize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def plot_noise_map(
    fit,
    mask=None,
    extract_array_from_mask=False,
    zoom_around_mask=False,
    positions=None,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Fit Noise-Map",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10,
    output_path=None,
    output_format="show",
    output_filename="fit_noise_map",
):
    """Plot the noise-map of a lens fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    image : datas.ccd.datas.CCD
        The datas-datas, which includes the observed datas, noise_map-map, PSF, signal-to-noise_map-map, etc.
    plot_origin : True
        If true, the origin of the datas's coordinate system is plotted as a 'x'.
    """

    noise_map = fit.noise_map(return_in_2d=True)

    array_plotters.plot_array(
        array=noise_map,
        mask=mask,
        extract_array_from_mask=extract_array_from_mask,
        zoom_around_mask=zoom_around_mask,
        positions=positions,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def plot_signal_to_noise_map(
    fit,
    mask=None,
    extract_array_from_mask=False,
    zoom_around_mask=False,
    positions=None,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Fit Signal-to-Noise-Map",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10,
    output_path=None,
    output_format="show",
    output_filename="fit_signal_to_noise_map",
):
    """Plot the noise-map of a lens fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    image : datas.ccd.datas.CCD
    The datas-datas, which includes the observed datas, signal_to_noise_map-map, PSF, signal-to-signal_to_noise_map-map, etc.
    plot_origin : True
    If true, the origin of the datas's coordinate system is plotted as a 'x'.
    """

    signal_to_noise_map = fit.signal_to_noise_map(return_in_2d=True)

    array_plotters.plot_array(
        array=signal_to_noise_map,
        mask=mask,
        extract_array_from_mask=extract_array_from_mask,
        zoom_around_mask=zoom_around_mask,
        positions=positions,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def plot_model_data(
    fit,
    mask=None,
    extract_array_from_mask=False,
    zoom_around_mask=False,
    positions=None,
    plot_mass_profile_centres=True,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Fit Model Image",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10,
    output_path=None,
    output_format="show",
    output_filename="fit_model_image",
):
    """Plot the model image of a fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    fit : datas.fitting.fitting.AbstractFitter
        The fit to the datas, which includes a list of every model image, residual_map, chi-squareds, etc.
    image_index : int
        The index of the datas in the datas-set of which the model image is plotted.
    """

    centres = get_mass_profile_centes(
        plot_mass_profile_centres=plot_mass_profile_centres, fit=fit
    )

    model_image = fit.model_image(return_in_2d=True)

    array_plotters.plot_array(
        array=model_image,
        mask=mask,
        extract_array_from_mask=extract_array_from_mask,
        zoom_around_mask=zoom_around_mask,
        positions=positions,
        centres=centres,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def plot_residual_map(
    fit,
    mask=None,
    extract_array_from_mask=False,
    zoom_around_mask=False,
    positions=None,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Fit Residuals",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10,
    output_path=None,
    output_format="show",
    output_filename="fit_residual_map",
):
    """Plot the residual-map of a lens fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    fit : datas.fitting.fitting.AbstractFitter
        The fit to the datas, which includes a list of every model image, residual_map, chi-squareds, etc.
    image_index : int
        The index of the datas in the datas-set of which the residual_map are plotted.
    """

    residual_map = fit.residual_map(return_in_2d=True)

    array_plotters.plot_array(
        array=residual_map,
        mask=mask,
        extract_array_from_mask=extract_array_from_mask,
        zoom_around_mask=zoom_around_mask,
        positions=positions,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def plot_normalized_residual_map(
    fit,
    mask=None,
    extract_array_from_mask=False,
    zoom_around_mask=False,
    positions=None,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Fit Normalized Residuals",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10,
    output_path=None,
    output_format="show",
    output_filename="fit_normalized_residual_map",
):
    """Plot the residual-map of a lens fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    fit : datas.fitting.fitting.AbstractFitter
        The fit to the datas, which includes a list of every model image, normalized_residual_map, chi-squareds, etc.
    image_index : int
        The index of the datas in the datas-set of which the normalized_residual_map are plotted.
    """

    normalized_residual_map = fit.normalized_residual_map(return_in_2d=True)

    array_plotters.plot_array(
        array=normalized_residual_map,
        mask=mask,
        extract_array_from_mask=extract_array_from_mask,
        zoom_around_mask=zoom_around_mask,
        positions=positions,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def plot_chi_squared_map(
    fit,
    mask=None,
    extract_array_from_mask=False,
    zoom_around_mask=False,
    positions=None,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Fit Chi-Squareds",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10,
    output_path=None,
    output_format="show",
    output_filename="fit_chi_squared_map",
):
    """Plot the chi-squared map of a lens fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    fit : datas.fitting.fitting.AbstractFitter
        The fit to the datas, which includes a list of every model image, residual_map, chi-squareds, etc.
    image_index : int
        The index of the datas in the datas-set of which the chi-squareds are plotted.
    """

    chi_squared_map = fit.chi_squared_map(return_in_2d=True)

    array_plotters.plot_array(
        array=chi_squared_map,
        mask=mask,
        extract_array_from_mask=extract_array_from_mask,
        zoom_around_mask=zoom_around_mask,
        positions=positions,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def plot_subtracted_image_of_plane(
    fit,
    plane_index,
    mask=None,
    extract_array_from_mask=False,
    zoom_around_mask=False,
    positions=None,
    image_plane_pix_grid=None,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Fit Model Image",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10,
    output_path=None,
    output_format="show",
    output_filename="fit_subtracted_image_of_plane",
):
    """Plot the model image of a specific plane of a lens fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    fit : datas.fitting.fitting.AbstractFitter
        The fit to the datas, which includes a list of every model image, residual_map, chi-squareds, etc.
    image_index : int
        The index of the datas in the datas-set of which the model image is plotted.
    plane_indexes : int
        The plane from which the model image is generated.
    """

    output_filename += "_" + str(plane_index)

    if fit.tracer.total_planes > 1:

        other_planes_model_images_2d = [
            model_image_2d
            for i, model_image_2d in enumerate(fit.model_image_2d_of_planes)
            if i != plane_index
        ]

        subtracted_image = fit.image(return_in_2d=True) - sum(
            other_planes_model_images_2d
        )

    else:

        subtracted_image = fit.image(return_in_2d=True)

    array_plotters.plot_array(
        array=subtracted_image,
        mask=mask,
        extract_array_from_mask=extract_array_from_mask,
        grid=image_plane_pix_grid,
        zoom_around_mask=zoom_around_mask,
        positions=positions,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def plot_model_image_of_plane(
    fit,
    plane_index,
    mask=None,
    extract_array_from_mask=False,
    zoom_around_mask=False,
    positions=None,
    plot_mass_profile_centres=True,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Model Image",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10,
    output_path=None,
    output_format="show",
    output_filename="fit_model_image_of_plane",
):
    """Plot the model image of a specific plane of a lens fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    fit : datas.fitting.fitting.AbstractFitter
        The fit to the datas, which includes a list of every model image, residual_map, chi-squareds, etc.
    plane_indexes : [int]
        The plane from which the model image is generated.
    """

    output_filename += "_" + str(plane_index)

    centres = get_mass_profile_centes(
        plot_mass_profile_centres=plot_mass_profile_centres, fit=fit
    )

    array_plotters.plot_array(
        array=fit.model_image_2d_of_planes[plane_index],
        mask=mask,
        extract_array_from_mask=extract_array_from_mask,
        zoom_around_mask=zoom_around_mask,
        positions=positions,
        centres=centres,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def plot_contribution_maps(
    fit,
    mask=None,
    extract_array_from_mask=False,
    zoom_around_mask=False,
    positions=None,
    as_subplot=False,
    units="arcsec",
    kpc_per_arcsec=None,
    figsize=(7, 7),
    aspect="square",
    cmap="jet",
    norm="linear",
    norm_min=None,
    norm_max=None,
    linthresh=0.05,
    linscale=0.01,
    cb_ticksize=10,
    cb_fraction=0.047,
    cb_pad=0.01,
    cb_tick_values=None,
    cb_tick_labels=None,
    title="Contributions",
    titlesize=16,
    xlabelsize=16,
    ylabelsize=16,
    xyticksize=16,
    mask_pointsize=10,
    position_pointsize=10,
    output_path=None,
    output_format="show",
    output_filename="fit_contribution_maps",
):
    """Plot the summed contribution maps of a hyper_galaxies-fit.

    Set *autolens.datas.array.plotters.array_plotters* for a description of all input parameters not described below.

    Parameters
    -----------
    fit : datas.fitting.fitting.AbstractLensHyperFit
        The hyper_galaxies-fit to the datas, which includes a list of every model image, residual_map, chi-squareds, etc.
    image_index : int
        The index of the datas in the datas-set of which the contribution_maps are plotted.
    """

    if len(fit.contribution_maps) > 1:
        contribution_map = sum(fit.contribution_maps)
    else:
        contribution_map = fit.contribution_maps[0]

    array_plotters.plot_array(
        array=contribution_map,
        mask=mask,
        extract_array_from_mask=extract_array_from_mask,
        zoom_around_mask=zoom_around_mask,
        positions=positions,
        as_subplot=as_subplot,
        units=units,
        kpc_per_arcsec=kpc_per_arcsec,
        figsize=figsize,
        aspect=aspect,
        cmap=cmap,
        norm=norm,
        norm_min=norm_min,
        norm_max=norm_max,
        linthresh=linthresh,
        linscale=linscale,
        cb_ticksize=cb_ticksize,
        cb_fraction=cb_fraction,
        cb_pad=cb_pad,
        cb_tick_values=cb_tick_values,
        cb_tick_labels=cb_tick_labels,
        title=title,
        titlesize=titlesize,
        xlabelsize=xlabelsize,
        ylabelsize=ylabelsize,
        xyticksize=xyticksize,
        mask_pointsize=mask_pointsize,
        position_pointsize=position_pointsize,
        output_path=output_path,
        output_format=output_format,
        output_filename=output_filename,
    )


def get_image_plane_pix_grid(should_plot_image_plane_pix, fit):

    if hasattr(fit, "inversion"):
        if (
            should_plot_image_plane_pix
            and fit.inversion.mapper.is_image_plane_pixelization
        ):
            return fit.tracer.pixelization_grids_of_planes_from_grid(grid=fit.grid)[-1]
    else:
        return None


def get_mask(fit, should_plot_mask):
    """Get the masks of the fit if the masks should be plotted on the fit.

    Parameters
    -----------
    fit : datas.fitting.fitting.AbstractLensHyperFit
        The fit to the datas, which includes a lisrt of every model image, residual_map, chi-squareds, etc.
    should_plot_mask : bool
        If *True*, the masks is plotted on the fit's datas.
    """
    if should_plot_mask:
        return fit.mask(return_in_2d=True)
    else:
        return None


def get_mass_profile_centes(plot_mass_profile_centres, fit):

    if not hasattr(fit, "tracer"):
        return None

    if plot_mass_profile_centres:
        return fit.tracer.image_plane.centres_of_galaxy_mass_profiles
    else:
        return None
