#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Martin Renou.
# Distributed under the terms of the Modified BSD License.

from contextlib import contextmanager

from traitlets import Float, Instance, List, Tuple, Unicode, observe

from ipywidgets import Color, DOMWidget, widget_serialization

from ._frontend import module_name, module_version

from .binary import array_to_binary


def to_camel_case(snake_str):
    """Turn a snake_case string into a camelCase one."""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class Canvas(DOMWidget):
    _model_name = Unicode('CanvasModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('CanvasView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    size = Tuple((700, 500), help='Size of the Canvas, this is not equal to the size of the view').tag(sync=True)

    fill_style = Color('black')
    stroke_style = Color('black')
    global_alpha = Float(1.0)

    font = Unicode('12px serif')
    textAlign = Unicode('start')
    textBaseline = Unicode('alphabetic')
    direction = Unicode('inherit')

    def __init__(self, *args, **kwargs):
        """Create a Canvas widget."""
        self.caching = kwargs.get('caching', False)
        self._commands_cache = []
        self._buffers_cache = []

        super(Canvas, self).__init__(*args, **kwargs)
        self.layout.width = str(self.size[0]) + 'px'
        self.layout.height = str(self.size[1]) + 'px'

    # Rectangles methods
    def fill_rect(self, x, y, width, height):
        """Draw a filled rectangle."""
        self._send_canvas_command('fillRect', (x, y, width, height))

    def stroke_rect(self, x, y, width, height):
        """Draw a rectangular outline."""
        self._send_canvas_command('strokeRect', (x, y, width, height))

    def clear_rect(self, x, y, width, height):
        """Clear the specified rectangular area, making it fully transparent."""
        self._send_canvas_command('clearRect', (x, y, width, height))

    def rect(self, x, y, width, height):
        """Draw a rectangle whose top-left corner is specified by (x, y) with the specified width and height."""
        self._send_canvas_command('rect', (x, y, width, height))

    # Paths methods
    def begin_path(self):
        """Call this method when you want to create a new path."""
        self._send_canvas_command('beginPath')

    def close_path(self):
        """Add a straight line from the current point to the start of the current path.

        If the shape has already been closed or has only one point, this function does nothing.
        This method doesn't draw anything to the canvas directly. You can render the path using the stroke() or fill() methods.
        """
        self._send_canvas_command('closePath')

    def stroke(self):
        """Stroke (outlines) the current path with the current stroke style."""
        self._send_canvas_command('stroke')

    def fill(self):
        """Fill the current or given path with the current fillStyle."""
        self._send_canvas_command('fill')

    def move_to(self, x, y):
        """Move the "pen" to the given (x, y) coordinates."""
        self._send_canvas_command('moveTo', (x, y))

    def line_to(self, x, y):
        """Add a straight line to the current path by connecting the path's last point to the specified (x, y) coordinates.

        Like other methods that modify the current path, this method does not directly render anything. To
        draw the path onto the canvas, you can use the fill() or stroke() methods.
        """
        self._send_canvas_command('lineTo', (x, y))

    def arc(self, x, y, radius, start_angle, end_angle, anticlockwise=False):
        """Create a circular arc centered at (x, y) with a radius of radius.

        The path starts at startAngle and ends at endAngle, and travels in the direction given by
        anticlockwise (defaulting to clockwise).
        """
        self._send_canvas_command('arc', (x, y, radius, start_angle, end_angle, anticlockwise))

    def arc_to(self, x1, y1, x2, y2, radius):
        """Add a circular arc to the current path, using the given control points and radius."""
        self._send_canvas_command('arcTo', (x1, y1, x2, y2, radius))

    def quadratic_curve_to(self, cp1x, cp1y, x, y):
        """Add a quadratic Bezier curve to the current path.

        It requires two points: the first one is a control point and the second one is the end point.
        The starting point is the latest point in the current path, which can be changed using move_to()
        before creating the quadratic Bezier curve.
        """
        self._send_canvas_command('quadraticCurveTo', (cp1x, cp1y, x, y))

    def bezier_curve_to(self, cp1x, cp1y, cp2x, cp2y, x, y):
        """Add a cubic Bezier curve to the current path.

        It requires three points: the first two are control points and the third one is the end point.
        The starting point is the latest point in the current path, which can be changed using move_to()
        before creating the Bezier curve.
        """
        self._send_canvas_command('bezierCurveTo', (cp1x, cp1y, cp2x, cp2y, x, y))

    # Text methods
    def fill_text(self, text, x, y, max_width=None):
        """Fill a given text at the given (x,y) position. Optionally with a maximum width to draw."""
        self._send_canvas_command('fillText', (text, x, y, max_width))

    def stroke_text(self, text, x, y, max_width=None):
        """Stroke a given text at the given (x,y) position. Optionally with a maximum width to draw."""
        self._send_canvas_command('strokeText', (text, x, y, max_width))

    # Image methods
    def put_image_data(self, image_data, dx, dy):
        """Draw an image on the Canvas.

        `image_data` being a NumPy array defining the image to draw
        and `x` and `y` the pixel position where to draw.
        This method is not affected by the canvas transformation matrix.
        """
        shape, image_buffer = array_to_binary(image_data)
        self._send_canvas_command('putImageData', ({'shape': shape}, dx, dy), (image_buffer, ))

    def clear(self):
        """Clear the entire canvas."""
        self._send_command({'name': 'clear'})

    def flush(self):
        """Flush all the cached commands."""
        if not self.caching:
            return

        self.send(self._commands_cache, self._buffers_cache)

        self.caching = False
        self._commands_cache = []
        self._buffers_cache = []

    @observe('fill_style', 'stroke_style', 'global_alpha', 'font', 'textAlign', 'textBaseline', 'direction')
    def _on_set_attr(self, change):
        command = {
            'name': 'set',
            'attr': to_camel_case(change.name),
            'value': change.new
        }
        self._send_command(command)

    def _send_canvas_command(self, name, args=[], buffers=[]):
        command = {
            'name': name,
            'n_buffers': len(buffers),
            'args': [arg for arg in args if arg is not None]
        }
        self._send_command(command, buffers)

    def _send_command(self, command, buffers=[]):
        if self.caching:
            self._commands_cache.append(command)
            self._buffers_cache += buffers
        else:
            self.send(command, buffers)


class MultiCanvas(DOMWidget):
    _model_name = Unicode('MultiCanvasModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('MultiCanvasView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    size = Tuple((700, 500), help='Size of the Canvas, this is not equal to the size of the view')

    _canvases = List(Instance(Canvas)).tag(sync=True, **widget_serialization)

    def __init__(self, n_canvases=3, *args, **kwargs):
        """Create a MultiCanvas widget with n_canvases Canvas widgets."""
        size = kwargs.get('size', (700, 500))

        super(MultiCanvas, self).__init__(*args, _canvases=[Canvas(size=size) for _ in range(n_canvases)], **kwargs)
        self.layout.width = str(size[0]) + 'px'
        self.layout.height = str(size[1]) + 'px'

    def __getitem__(self, key):
        """Access one of the Canvas instances."""
        return self._canvases[key]

    @observe('size')
    def _on_size_change(self, change):
        for canvas in self._canvases:
            canvas.size = change.new


@contextmanager
def hold_canvas(canvas):
    """Hold any drawing on the canvas, and perform only one draw command at the end."""
    canvas.caching = True
    yield
    canvas.flush()
