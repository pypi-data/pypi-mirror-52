import os.path
from glob import glob
import numpy as np
import inspect
from pathlib import Path

from qtpy.QtCore import QCoreApplication, Qt, QSize
from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QFileDialog,
    QSplitter,
)
from qtpy.QtWidgets import QStackedWidget, QSizePolicy
from qtpy.QtGui import QCursor, QPixmap
from qtpy import API_NAME
from vispy.scene import SceneCanvas, PanZoomCamera, ArcballCamera
from vispy.visuals.transforms import ChainTransform
from vispy.app import use_app

from .qt_dims import QtDims
from .qt_layerlist import QtLayerList
from ..resources import resources_dir
from ..util.theme import template
from ..util.misc import is_multichannel
from ..util.keybindings import components_to_key_combo
from ..util.io import read

from .qt_controls import QtControls
from .qt_layer_buttons import QtLayersButtons
from .qt_console import QtConsole
from .._vispy import create_vispy_visual


# set vispy application to the appropriate qt backend
use_app(API_NAME)


class QtViewer(QSplitter):
    with open(os.path.join(resources_dir, 'stylesheet.qss'), 'r') as f:
        raw_stylesheet = f.read()

    def __init__(self, viewer):
        super().__init__()

        QCoreApplication.setAttribute(
            Qt.AA_UseStyleSheetPropagationInWidgetStyles, True
        )

        self.viewer = viewer
        self.dims = QtDims(self.viewer.dims)
        self.controls = QtControls(self.viewer)
        self.layers = QtLayerList(self.viewer.layers)
        self.buttons = QtLayersButtons(self.viewer)
        self.console = QtConsole({'viewer': self.viewer})

        # This dictionary holds the corresponding vispy visual for each layer
        self.layer_to_visual = {}

        if self.console.shell is not None:
            self.console.style().unpolish(self.console)
            self.console.style().polish(self.console)
            self.console.hide()
            self.buttons.consoleButton.clicked.connect(
                lambda: self._toggle_console()
            )
        else:
            self.buttons.consoleButton.setEnabled(False)

        self.canvas = SceneCanvas(keys=None, vsync=True)
        self.canvas.native.setMinimumSize(QSize(200, 200))

        self.canvas.connect(self.on_mouse_move)
        self.canvas.connect(self.on_mouse_press)
        self.canvas.connect(self.on_mouse_release)
        self.canvas.connect(self.on_key_press)
        self.canvas.connect(self.on_key_release)
        self.canvas.connect(self.on_draw)

        self.view = self.canvas.central_widget.add_view()
        self._update_camera()

        center = QWidget()
        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(15, 20, 15, 10)
        center_layout.addWidget(self.canvas.native)
        center_layout.addWidget(self.dims)
        center.setLayout(center_layout)

        right = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.layers)
        right_layout.addWidget(self.buttons)
        right.setLayout(right_layout)
        right.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        left = self.controls

        top = QWidget()
        top_layout = QHBoxLayout()
        top_layout.addWidget(left)
        top_layout.addWidget(center)
        top_layout.addWidget(right)
        top.setLayout(top_layout)

        self.setOrientation(Qt.Vertical)
        self.addWidget(top)

        if self.console.shell is not None:
            self.addWidget(self.console)

        self._last_visited_dir = str(Path.home())

        self._cursors = {
            'disabled': QCursor(
                QPixmap(':/icons/cursor/cursor_disabled.png').scaled(20, 20)
            ),
            'cross': Qt.CrossCursor,
            'forbidden': Qt.ForbiddenCursor,
            'pointing': Qt.PointingHandCursor,
            'standard': QCursor(),
        }

        self._update_palette(viewer.palette)

        self._key_release_generators = {}

        self.viewer.events.interactive.connect(self._on_interactive)
        self.viewer.events.cursor.connect(self._on_cursor)
        self.viewer.events.reset_view.connect(self._on_reset_view)
        self.viewer.events.palette.connect(
            lambda event: self._update_palette(event.palette)
        )
        self.viewer.layers.events.reordered.connect(self._reorder_layers)
        self.viewer.layers.events.added.connect(self._add_layer)
        self.viewer.layers.events.removed.connect(self._remove_layer)
        self.viewer.dims.events.camera.connect(
            lambda event: self._update_camera()
        )

        self.setAcceptDrops(True)

    def _add_layer(self, event):
        """When a layer is added, set its parent and order."""
        layers = event.source
        layer = event.item
        vispy_layer = create_vispy_visual(layer)
        vispy_layer.camera = self.view.camera
        vispy_layer.node.parent = self.view.scene
        vispy_layer.order = len(layers)
        self.layer_to_visual[layer] = vispy_layer

    def _remove_layer(self, event):
        """When a layer is removed, remove its parent."""
        layer = event.item
        vispy_layer = self.layer_to_visual[layer]
        vispy_layer.node.transforms = ChainTransform()
        vispy_layer.node.parent = None
        del self.layer_to_visual[layer]

    def _reorder_layers(self, event):
        """When the list is reordered, propagate changes to draw order."""
        for i, layer in enumerate(self.viewer.layers):
            vispy_layer = self.layer_to_visual[layer]
            vispy_layer.order = i
        self.canvas._draw_order.clear()
        self.canvas.update()

    def _update_camera(self):
        if self.viewer.dims.ndisplay == 3:
            # Set a 3D camera
            if not isinstance(self.view.camera, ArcballCamera):
                self.view.camera = ArcballCamera(name="ArcballCamera")
                # flip y-axis to have correct alignment
                self.view.camera.flip = (0, 1, 0)

                self.view.camera.viewbox_key_event = viewbox_key_event
                self.viewer.reset_view()
        else:
            # Set 2D camera
            if not isinstance(self.view.camera, PanZoomCamera):
                self.view.camera = PanZoomCamera(
                    aspect=1, name="PanZoomCamera"
                )
                # flip y-axis to have correct alignment
                self.view.camera.flip = (0, 1, 0)

                self.view.camera.viewbox_key_event = viewbox_key_event
                self.viewer.reset_view()

    def screenshot(self):
        """Take currently displayed screen and convert to an image array.

        Returns
        -------
        image : array
            Numpy array of type ubyte and shape (h, w, 4). Index [0, 0] is the
            upper-left corner of the rendered region.
        """
        img = self.canvas.native.grabFramebuffer()
        b = img.constBits()
        h, w, c = img.height(), img.width(), 4

        # As vispy doesn't use qtpy we need to reconcile the differences
        # between the `QImage` API for `PySide2` and `PyQt5` on how to convert
        # a QImage to a numpy array.
        if API_NAME == 'PySide2':
            arr = np.array(b).reshape(h, w, c)
        else:
            b.setsize(h * w * c)
            arr = np.frombuffer(b, np.uint8).reshape(h, w, c)

        # Format of QImage is ARGB32_Premultiplied, but color channels are
        # reversed.
        arr = arr[:, :, [2, 1, 0, 3]]
        return arr

    def _open_images(self):
        """Adds image files from the menubar."""
        filenames, _ = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Select image(s)...',
            directory=self._last_visited_dir,  # home dir by default
        )
        self._add_files(filenames)

    def _add_files(self, filenames):
        """Adds an image layer to the viewer.

        Whether the image is multichannel is determined by
        :func:`napari.util.misc.is_multichannel`.

        If multiple images are selected, they are stacked along the 0th
        axis.

        Parameters
        -------
        filenames : list
            List of filenames to be opened
        """
        if len(filenames) > 0:
            image = read(filenames)
            self.viewer.add_image(
                image, multichannel=is_multichannel(image.shape)
            )
            self._last_visited_dir = os.path.dirname(filenames[0])

    def _on_interactive(self, event):
        self.view.interactive = self.viewer.interactive

    def _on_cursor(self, event):
        cursor = self.viewer.cursor
        size = self.viewer.cursor_size
        if cursor == 'square':
            if size < 10 or size > 300:
                q_cursor = self._cursors['cross']
            else:
                q_cursor = QCursor(
                    QPixmap(':/icons/cursor/cursor_square.png').scaledToHeight(
                        size
                    )
                )
        else:
            q_cursor = self._cursors[cursor]
        self.canvas.native.setCursor(q_cursor)

    def _on_reset_view(self, event):
        if isinstance(self.view.camera, ArcballCamera):
            self.view.camera.center = event.center
            self.view.camera.scale_factor = event.scale_factor
        else:
            # Assumes default camera has the same properties as PanZoomCamera
            self.view.camera.rect = event.viewbox

    def _update_palette(self, palette):
        # template and apply the primary stylesheet
        themed_stylesheet = template(self.raw_stylesheet, **palette)
        self.console.style_sheet = themed_stylesheet
        self.console.syntax_style = palette['syntax_style']
        self.setStyleSheet(themed_stylesheet)
        self.canvas.bgcolor = palette['canvas']

    def _toggle_console(self):
        """Toggle console visible and not visible."""
        self.console.setVisible(not self.console.isVisible())
        self.buttons.consoleButton.setProperty(
            'expanded', self.console.isVisible()
        )
        self.buttons.consoleButton.style().unpolish(self.buttons.consoleButton)
        self.buttons.consoleButton.style().polish(self.buttons.consoleButton)

    def on_mouse_move(self, event):
        """Called whenever mouse moves over canvas.
        """
        layer = self.viewer.active_layer
        if layer is not None:
            self.layer_to_visual[layer].on_mouse_move(event)

    def on_mouse_press(self, event):
        """Called whenever mouse pressed in canvas.
        """
        layer = self.viewer.active_layer
        if layer is not None:
            self.layer_to_visual[layer].on_mouse_press(event)

    def on_mouse_release(self, event):
        """Called whenever mouse released in canvas.
        """
        layer = self.viewer.active_layer
        if layer is not None:
            self.layer_to_visual[layer].on_mouse_release(event)

    def on_key_press(self, event):
        """Called whenever key pressed in canvas.
        """
        if (
            event.native.isAutoRepeat()
            and event.key.name not in ['Up', 'Down', 'Left', 'Right']
        ) or event.key is None:
            # pass is no key is present or if key is held down, unless the
            # key being held down is one of the navigation keys
            return

        comb = components_to_key_combo(event.key.name, event.modifiers)

        layer = self.viewer.active_layer

        if layer is not None and comb in layer.keymap:
            parent = layer
        elif comb in self.viewer.keymap:
            parent = self.viewer
        else:
            return

        func = parent.keymap[comb]
        gen = func(parent)

        if inspect.isgeneratorfunction(func):
            try:
                next(gen)
            except StopIteration:  # only one statement
                pass
            else:
                self._key_release_generators[event.key] = gen

    def on_key_release(self, event):
        """Called whenever key released in canvas.
        """
        try:
            next(self._key_release_generators[event.key])
        except (KeyError, StopIteration):
            pass

    def on_draw(self, event):
        """Called whenever drawn in canvas. Called for all layers, not just top
        """
        for layer in self.viewer.layers:
            self.layer_to_visual[layer].on_draw(event)

    def keyPressEvent(self, event):
        self.canvas._backend._keyEvent(self.canvas.events.key_press, event)
        event.accept()

    def keyReleaseEvent(self, event):
        self.canvas._backend._keyEvent(self.canvas.events.key_release, event)
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Add local files and web URLS with drag and drop."""
        filenames = []
        for url in event.mimeData().urls():
            path = url.toString()
            if os.path.isfile(path):
                filenames.append(path)
            elif os.path.isdir(path):
                filenames = filenames + list(glob(os.path.join(path, '*')))
            else:
                filenames.append(path)
        self._add_files(filenames)


def viewbox_key_event(event):
    """ViewBox key event handler
    Parameters
    ----------
    event : instance of Event
        The event.
    """
    return
