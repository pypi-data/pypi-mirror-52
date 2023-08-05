from .viewer import Viewer


def view(
    *images,
    title='napari',
    metadata=None,
    multichannel=None,
    contrast_limits=None,
    **named_images,
):
    """View one or more input images.
    Parameters
    ----------
    *images : ndarray
        Arrays to render as image layers.
    title : string, optional
        The title of the viewer window.
    meta : dictionary, optional
        A dictionary of metadata attributes. If multiple images are provided,
        the metadata applies to all of them.
    multichannel : bool, optional
        Whether to consider the last dimension of the image(s) as channels
        rather than spatial attributes. If not provided, napari will attempt
        to make an educated guess. If provided, and multiple images are given,
        the same value applies to all images.
    contrast_limits : list (2,)
        Color limits to be used for determining the colormap bounds for
        luminance images. If not passed is calculated as the min and max of
        the image. Passing a value prevents this calculation which can be useful
        when working with very large datasets that are dynamically loaded.
        If provided, and multiple images are given, the same value applies to
        all images.
    **named_images : dict of str -> ndarray, optional
        Arrays to render as image layers, keyed by layer name.
    Returns
    -------
    viewer : napari.Viewer
        A Viewer widget displaying the images.
    Notes
    -----
    This convenience function is used to view one or few images with identical
    parameters (colormap etc). To customize each image layer, either use the
    :class:`napari.Viewer` class (preferred), or update the layers directly on
    the returned :class:`napari.Viewer` object.
    """
    viewer = Viewer(title=title)
    for image in images:
        viewer.add_image(
            image,
            metadata=metadata,
            multichannel=multichannel,
            contrast_limits=contrast_limits,
        )
    for name, image in named_images.items():
        viewer.add_image(
            image,
            metadata=metadata,
            multichannel=multichannel,
            contrast_limits=contrast_limits,
            name=name,
        )
    return viewer
