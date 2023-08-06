"""`beams.utils.py`"""

import math

import numpy as np


def rgb_to_rgba(rgb_str, alpha):
    rgb = rgb_str.split('rgb(')[1].split(')')[0].split(',')
    rgba = rgb + [' ' + str(alpha)]
    rgba_str = ','.join(rgba)
    rgba_str = 'rgba({})'.format(rgba_str)
    return rgba_str


def get_circle_trace(radius, origin):
    x, y = [], []
    N = 100
    for i in range(N + 1):
        theta_i = (i / N) * 2 * math.pi
        x.append(radius * math.cos(theta_i) + origin[0])
        y.append(radius * math.sin(theta_i) + origin[1])

    out = {
        'x': x,
        'y': y,
        'mode': 'lines',
    }
    return out


def get_plotly_arrow_shapes(point, width=10, length=2, line_width=1, down=True):

    tri_height = -np.cos(np.deg2rad(30)) * width
    length *= -1

    if down:
        tri_height *= -1
        length *= -1

    half_width = width / 2
    corner_1 = [-half_width, tri_height]
    corner_2 = [half_width, tri_height]

    path = (
        'M0 0 '
        'L{} {} '
        'L{} {} '
        'L0 0 '
        'Z'
    ).format(*corner_1, *corner_2)

    arrow_head = {
        'type': 'path',
        'path': path,
        'fillcolor': 'black',
        'line': {
            'width': 0,
        },
        'ysizemode': 'pixel',
        'xsizemode': 'pixel',
        'xanchor': point[0],
        'yanchor': point[1],
    }

    arrow_stem = {
        'type': 'line',
        'x0': point[0],
        'y0': point[1],
        'x1': point[0],
        'y1': point[1] + length,
        'ysizemode': 'scaled',
        'xsizemode': 'scaled',
        'line': {
            'color': 'black',
            'width': line_width,
        }
    }

    out = [
        arrow_head,
        arrow_stem,
    ]

    return out


def get_plotly_dimension_label(position, width=None, height=None, line_props=None,
                               lug_length=10, text=None, font=None, text_pos=None,
                               text_shift=10):
    """
    Parameters
    ----------
    position : list of length two
        (x, y) coordinates of the centre of the dimension label.
    text_post : int, optional
        If 0, align text to left or bottom of line. If 1, align text to right or top.


    """

    if not line_props:
        line_props = {}
    if text:
        if not font:
            font = {}
        if not text_pos:
            text_pos = 0

    if (width is None and height is None) or (width is not None and height is not None):
        msg = 'Specify exactly one of `width` and `height`'
        raise ValueError(msg)

    x, y = position

    if width:
        x_max = x + (width / 2)
        x_min = x - (width / 2)
        text_x_anchor = 'center'
        text_y_anchor = 'bottom' if text_pos else 'top'
        xshift = 0
        yshift = (1 if text_pos else -1) * text_shift
        shapes = [
            {
                'type': 'line',
                'x0': x_min,
                'y0': y,
                'x1': x_max,
                'y1': y,
                'line': line_props,
            },
            {
                'type': 'line',
                'x0': x_min,
                'x1': x_min,
                'y0': -lug_length,
                'y1': lug_length,
                'yanchor': y,
                'ysizemode': 'pixel',
                'line': line_props,
            },
            {
                'type': 'line',
                'x0': x_max,
                'x1': x_max,
                'y0': -lug_length,
                'y1': lug_length,
                'yanchor': y,
                'ysizemode': 'pixel',
                'line': line_props,
            },
        ]
    else:
        y_max = y + (height / 2)
        y_min = y - (height / 2)
        text_x_anchor = 'left' if text_pos else 'right'
        text_y_anchor = 'middle'
        xshift = (1 if text_pos else -1) * text_shift
        yshift = 0
        shapes = [
            {
                'type': 'line',
                'x0': x,
                'y0': y_min,
                'x1': x,
                'y1': y_max,
                'line': line_props,
            },
            {
                'type': 'line',
                'x0': -lug_length,
                'x1': lug_length,
                'y0': y_min,
                'y1': y_min,
                'xanchor': x,
                'xsizemode': 'pixel',
                'line': line_props,
            },
            {
                'type': 'line',
                'x0': -lug_length,
                'x1': lug_length,
                'y0': y_max,
                'y1': y_max,
                'xanchor': x,
                'xsizemode': 'pixel',
                'line': line_props,
            },
        ]

    annots = []
    if text:
        annots.append(
            {
                'text': text,
                'x': x,
                'y': y,
                'xshift': xshift,
                'yshift': yshift,
                'xanchor': text_x_anchor,
                'yanchor': text_y_anchor,
                'showarrow': False,
                'font': font,
                'bgcolor': 'rgba(255, 255, 255, 0.8)',
            }
        )

    return shapes, annots
