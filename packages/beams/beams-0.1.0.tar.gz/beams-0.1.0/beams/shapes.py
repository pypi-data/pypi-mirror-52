'`beams.shapes.py`'

import math

import numpy as np
from plotly import graph_objects as go
from plotly.colors import DEFAULT_PLOTLY_COLORS

from beams.utils import get_plotly_dimension_label


def rgb_to_rgba(rgb_str, alpha):
    rgb = rgb_str.split('rgb(')[1].split(')')[0].split(',')
    rgba = rgb + [' ' + str(alpha)]
    rgba_str = ','.join(rgba)
    rgba_str = 'rgba({})'.format(rgba_str)
    return rgba_str


def mag(vec):
    return math.sqrt(sum([i**2 for i in vec]))


def parallel_axis_theoerm(I_0, area, distance):
    """Get the second moment of area of a shape about an axis parallel 
    to a centroidal axis, given the distance between the axes and the second
    moment of area about the centroidal axis."""

    return I_0 + area * (distance ** 2)


class Shape(object):

    name = None
    visual = None
    parents = None
    negative = False

    def _get_shape_trace_props(self):

        if self.negative:
            fill_colour = CrossSection.FIG_NEG_FILL_COLOUR
        else:
            fill_colour = CrossSection.FIG_FILL_COLOUR

        name = ' ({})'.format(self.name) if self.name else ''
        cent = self.get_centroid()

        return (name, fill_colour, cent)

    @property
    def centroid(self):
        pass

    @property
    def x_mid(self):
        return (self.x_min + self.x_max) / 2

    @property
    def y_mid(self):
        return (self.y_min + self.y_max) / 2

    @property
    def area_sign(self):
        if self.negative:
            return -1
        else:
            return 1

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, origin):
        if not origin:
            origin = [0, 0]
        self._origin = origin

        if self.visual or any([i[0].visual for i in self.parents or []]):
            plot_traces = self._get_plot_traces()

        if self.visual:
            # Update FigureWidget
            with self.visual.batch_animate():
                for idx, i in enumerate(plot_traces):
                    self.visual.data[idx].update(i)

        for i in self.parents or []:
            if i[0].visual:
                # Update FigureWidgets of any CrossSection that contains this shape:
                with i[0].visual.batch_animate():
                    for j_idx, j in zip(i[1], plot_traces):
                        i[0].visual.data[j_idx].update(j)

    def translate(self, x, y):
        'Translate shape in the x and y directions.'
        self.origin = [
            self.origin[0] + x,
            self.origin[1] + y,
        ]
        return self

    def align_x(self, position='centre', x=0):
        'Align the left, centre or right of the object to a given x-coordinate.'
        if position == 'left':
            shift = x - self.x_min
        elif position == 'centre':
            shift = x - self.x_mid
        elif position == 'right':
            shift = x - self.x_max
        self.translate(shift, 0)
        return self

    def align_y(self, position, y=0):
        if position == 'bottom':
            shift = y - self.y_min
        elif position == 'middle':
            shift = y - self.y_mid
        elif position == 'top':
            shift = y - self.y_max
        self.translate(0, shift)
        return self

    def rotate(self, angle):
        'Rotate about the centroid.'
        return self

    def show(self, axes=None):
        if not axes:
            axes = []
        if not self.visual:
            data = self._get_plot_traces()
            shapes = []
            for i in axes:
                shapes.append(i.get_plot_shape())
            layout = {
                'xaxis': {
                    'scaleanchor': 'y',
                },
                'shapes': shapes,
            }
            fig = go.FigureWidget(data=data, layout=layout)
            self.visual = fig
        return self.visual

    @staticmethod
    def get_centroid(anchor, cent_from_anchor, x, y):
        cent = [
            anchor[0] - x + cent_from_anchor[0],
            anchor[1] - y + cent_from_anchor[1],
        ]
        return cent

    def get_zeroth_area_moment(self):
        return self.area

    def get_first_area_moment(self, axis):
        dist = axis.distance_from_point(self.get_centroid())
        return dist * self.area

    def get_second_area_moment(self, axis):
        'Use parallel axis theorem to get 2nd area moment about an axis parallel to a centroidal axis.'

        cent = self.get_centroid()
        cent_second_mom = self.get_centroidal_second_area_moment(axis)
        second_mom = parallel_axis_theoerm(
            cent_second_mom, self.area, axis.distance_from_point(cent))

        return second_mom

    def get_centroidal_xaxis(self):
        cent = self.get_centroid()
        xaxis = XAxis(y=cent[1])
        return xaxis

    def get_centroidal_yaxis(self):
        cent = self.get_centroid()
        yaxis = YAxis(x=cent[0])
        return yaxis

    def get_dimension_labels(self, width_offset=None, height_offset=None, width_side='bottom',
                             height_side='left', line_props=None, font=None):

        width = self.x_max - self.x_min
        if width_offset is None:
            width_offset = 0.1 * width

        height = self.y_max - self.y_min
        if height_offset is None:
            height_offset = 0.1 * height

        width_text_pos = 1
        if width_side == 'bottom':
            width_offset *= -1
            width_text_pos = 0

        height_text_pos = 1
        if height_side == 'left':
            height_offset *= -1
            height_text_pos = 0

        width_pos = [
            self.x_mid,
            (self.y_min if width_side == 'bottom' else self.y_max) + width_offset,
        ]

        w_shapes, w_annots = get_plotly_dimension_label(
            position=width_pos,
            width=width,
            line_props=line_props,
            text='{:.2f} m'.format(width),
            text_pos=width_text_pos,
            font=font,
        )

        height_pos = [
            (self.x_min if height_side == 'left' else self.x_max) + height_offset,
            self.y_mid,
        ]

        h_shapes, h_annots = get_plotly_dimension_label(
            position=height_pos,
            height=height,
            line_props=line_props,
            text='{:.2f} m'.format(height),
            text_pos=height_text_pos,
            font=font,
        )

        annots = w_annots + h_annots
        shapes = w_shapes + h_shapes

        return annots, shapes


class Circle(Shape):

    def __init__(self, radius, origin=None, name=None, negative=False):
        self.radius = radius
        self.origin = origin
        self.name = name
        self._colour = None
        self.negative = negative

    def __repr__(self):
        out = (
            '{}('
            'radius={!r}, '
            'height={!r}, '
            'negative={!r}'
            ')'
        ).format(
            self.__class__.__name__,
            self.radius,
            self.origin,
            self.negative,
        )
        return out

    @property
    def x_min(self):
        return self.origin[0] - self.radius

    @property
    def x_max(self):
        return self.origin[0] + self.radius

    @property
    def y_min(self):
        return self.origin[1] - self.radius

    @property
    def y_max(self):
        return self.origin[1] + self.radius

    @property
    def area(self):
        return math.pi * self.radius**2

    def get_centroid(self, x=0, y=0):
        'Get the x and y distance to the centroid from a given (x, y) coordinate.'
        anchor = [self.x_min, self.y_min]
        cent_from_anchor = [self.radius, self.radius]
        return super().get_centroid(anchor, cent_from_anchor, x, y)

    def get_centroidal_second_area_moment(self, axis):
        'Get 2nd area moment about the x or y-axis through the centroid.'

        if isinstance(axis, (XAxis, YAxis)):
            return (math.pi * self.radius ** 4) / 4
        else:
            raise ValueError('Bad axis')

    def _get_plot_traces(self, centroids):

        name, fill_colour, cent = self._get_shape_trace_props()

        x, y = [], []
        N = 100
        for i in range(N + 1):
            theta_i = (i / N) * 2 * math.pi
            x.append(self.radius * math.cos(theta_i) + self.origin[0])
            y.append(self.radius * math.sin(theta_i) + self.origin[1])

        out = [
            {
                'x': x,
                'y': y,
                'mode': 'lines',
                'name': 'circle' + name,
                'fill': 'toself',
                'fillcolor': fill_colour,
                'line': {
                    'color': CrossSection.FIG_OUTLINE_COLOUR,
                },
            },
        ]

        if centroids:
            out.append({
                'x': [cent[0]],
                'y': [cent[1]],
                'mode': 'markers',
                'name': 'circle centroid' + name,
                'marker': {
                    'color': CrossSection.FIG_OUTLINE_COLOUR,
                },
            })

        return out


class Rectangle(Shape):

    def __init__(self, width, height, origin=None, name=None, negative=False):
        self.width = width
        self.height = height
        self.origin = origin
        self.name = name
        self._colour = None
        self.negative = negative

    def __repr__(self):
        out = (
            '{}('
            'width={!r}, '
            'height={!r}, '
            'origin={!r}, '
            'negative={!r}'
            ')'
        ).format(
            self.__class__.__name__,
            self.width,
            self.height,
            self.origin,
            self.negative,
        )
        return out

    @property
    def x_min(self):
        return self.origin[0] - (self.width / 2)

    @property
    def x_max(self):
        return self.origin[0] + (self.width / 2)

    @property
    def y_min(self):
        return self.origin[1] - (self.height / 2)

    @property
    def y_max(self):
        return self.origin[1] + (self.height / 2)

    @property
    def area(self):
        return self.width * self.height

    def get_centroid(self, x=0, y=0):
        'Get the x and y distance to the centroid from a given (x, y) coordinate.'
        # Centroid defined in a coord system where (x_min, y_min) is at the origin:
        anchor = [self.x_min, self.y_min]
        cent_from_anchor = [self.width / 2, self.height / 2]
        return super().get_centroid(anchor, cent_from_anchor, x, y)

    def get_centroidal_second_area_moment(self, axis):
        'Get 2nd area moment about the x or y-axis through the centroid.'

        if isinstance(axis, XAxis):
            return (self.width * self.height ** 3) / 12
        elif isinstance(axis, YAxis):
            return (self.height * self.width ** 3) / 12
        else:
            raise ValueError('Bad axis')

    def _get_plot_traces(self, centroids):

        name, fill_colour, cent = self._get_shape_trace_props()
        out = [
            {
                'x': [self.x_min, self.x_max, self.x_max, self.x_min, self.x_min],
                'y': [self.y_min, self.y_min, self.y_max, self.y_max, self.y_min],
                'mode': 'lines',
                'name': 'rectangle' + name,
                'fill': 'toself',
                'fillcolor': fill_colour,
                'line': {
                    'color': CrossSection.FIG_OUTLINE_COLOUR,
                },
            },
        ]
        if centroids:
            out.append({
                'x': [cent[0]],
                'y': [cent[1]],
                'mode': 'markers',
                'name': 'centroid' + name,
                'marker': {
                    'color': CrossSection.FIG_OUTLINE_COLOUR,
                },
            })
        return out


class CrossSection(object):

    FIG_FONT_SIZE = 15
    FIG_FONT = 'Courier'
    FIG_FILL_COLOUR = 'silver'
    FIG_NEG_FILL_COLOUR = 'rgb(255, 255, 255)'
    FIG_OUTLINE_COLOUR = 'rgb(90, 90, 90)'
    FIG_DIMENSION_LABEL_LINE = {
        'width': 1.5,
        'color': 'gray',
        'dash': 'dot',
    }
    visual = None

    def __init__(self, *shapes, figure_width=700):
        self.figure_width = figure_width
        self.shapes = list(shapes)
        for i in self.shapes:
            if not i.parents:
                i.parents = [[self, None]]
            else:
                i.parents.append([self, None])

    def __repr__(self):
        out = (
            '{}('
            'shapes={!r}'
            ')'
        ).format(
            self.__class__.__name__,
            self.shapes,
        )
        return out

    @property
    def x_min(self):
        'Minimum x coordinate of all shapes.'
        x_min = self.shapes[0].x_min
        for i in self.shapes[1:]:
            if i.x_min < x_min:
                x_min = i.x_min
        return x_min

    @property
    def x_max(self):
        'Maximum x coordinate of all shapes.'
        x_max = self.shapes[0].x_max
        for i in self.shapes[1:]:
            if i.x_max > x_max:
                x_max = i.x_max
        return x_max

    @property
    def x_mid(self):
        'Middle x coordinate of composite shape.'
        return (self.x_min + self.x_max) / 2

    @property
    def y_min(self):
        'Minimum y coordinate of all shapes.'
        y_min = self.shapes[0].y_min
        for i in self.shapes[1:]:
            if i.y_min < y_min:
                y_min = i.y_min
        return y_min

    @property
    def y_max(self):
        'Maximum y coordinate of all shapes.'
        y_max = self.shapes[0].y_max
        for i in self.shapes[1:]:
            if i.y_max > y_max:
                y_max = i.y_max
        return y_max

    @property
    def y_mid(self):
        'Middle y coordinate of composite shape.'
        return (self.y_min + self.y_max) / 2

    @property
    def area(self):
        tot = 0
        for i in self.shapes:
            tot += (i.area_sign * i.area)
        return tot

    @property
    def stack_y_idx(self):
        mid_points = [i.y_mid for i in self.shapes]
        return np.argsort(mid_points)

    @property
    def overlap_x_idx(self):
        out = {i: [] for i in range(len(self.shapes))}
        for i_idx, i in enumerate(self.shapes):
            for j_idx, j in enumerate(self.shapes):
                if i is j:
                    continue
                if (
                    round(j.x_min, 5) < round(i.x_min, 5) < round(j.x_max, 5) or
                    round(j.x_min, 5) < round(i.x_max, 5) < round(j.x_max, 5) or
                    round(i.x_min, 5) < round(j.x_min, 5) < round(i.x_max, 5) or
                    round(i.x_min, 5) < round(j.x_max, 5) < round(i.x_max, 5)
                ):
                    out[i_idx].append(j_idx)

        return out

    def get_overlap_groups(self, overlap_idx):
        all_idx = list(overlap_idx.keys())
        added_idx = []
        all_groups = []
        while all_idx:
            grp = []
            for i, i_overlap in overlap_idx.items():
                if i in added_idx:
                    continue
                add = True
                for j in grp:
                    if j in i_overlap:
                        add = False
                        break
                if add:
                    grp.append(i)
                    added_idx.append(i)
                    all_idx.remove(i)
            all_groups.append(grp)
        return all_groups

    @property
    def overlap_y_idx(self):
        out = {i: [] for i in range(len(self.shapes))}
        for i_idx, i in enumerate(self.shapes):
            for j_idx, j in enumerate(self.shapes):
                if i is j:
                    continue
                if (
                    round(j.y_min, 5) < round(i.y_min, 5) < round(j.y_max, 5) or
                    round(j.y_min, 5) < round(i.y_max, 5) < round(j.y_max, 5) or
                    round(i.y_min, 5) < round(j.y_min, 5) < round(i.y_max, 5) or
                    round(i.y_min, 5) < round(j.y_max, 5) < round(i.y_max, 5)
                ):
                    out[i_idx].append(j_idx)

        return out

    def show(self, axes=None, centroids=True):

        if not axes:
            axes = []

        data = self._get_plot_traces(centroids)
        shapes = []
        for i in axes:
            shapes.append(i.get_plot_shape())

        dim_annots, dim_shapes = self.get_dimension_labels(
            line_props=CrossSection.FIG_DIMENSION_LABEL_LINE,
            font={'family': CrossSection.FIG_FONT,
                  'size': CrossSection.FIG_FONT_SIZE},
            figure_width=self.figure_width,
        )
        layout = {
            'xaxis': {
                'scaleanchor': 'y',
                'showgrid': False,
                'showticklabels': False,
                'zeroline': False,
                'range': [
                    self.x_min - (0.8 * (self.x_max - self.x_min)),
                    self.x_max + (0.8 * (self.x_max - self.x_min)),
                ],
            },
            'yaxis': {
                'showgrid': False,
                'showticklabels': False,
                'zeroline': False,
            },
            'margin': {
                'l': 0,
                'r': 0,
            },
            'showlegend': False,
            'shapes': shapes + dim_shapes,
            'annotations': dim_annots,
            'width': self.figure_width,
            'template': 'none',

        }
        fig = go.FigureWidget(data=data, layout=layout)

        return fig

    def _get_plot_traces(self, centroids):
        out = []
        for idx, i in enumerate(self.shapes):
            i_traces = i._get_plot_traces(centroids)
            trace_idx = (len(out), len(out) + len(i_traces) - 1)
            for j in i.parents:
                if j[0] == self:
                    j[1] = trace_idx
            out.extend(i_traces)

        if centroids:
            out.append(self._get_centroid_trace())
        return out

    def _get_centroid_trace(self):
        c = self.get_centroid()
        return {
            'x': [c[0]],
            'y': [c[1]],
            'mode': 'markers',
            'marker': {
                'symbol': 'square',
                'size': 8,
            },
            'name': 'Overall centroid',
        }

    def _update_centroid(self):
        if self.visual:
            with self.visual.batch_animate():
                self.visual.data[-1].update({**self._get_centroid_trace()})

    def align_x(self, position='centre', x=0):
        'Align the left, centre or right of all objects to a given x-coordinate.'
        for i in self.shapes:
            i.align_x(position, x)
        return self

    def align_y(self, position='middle', y=0):
        'Align the left, centre or right of all objects to a given x-coordinate.'
        for i in self.shapes:
            i.align_y(position, y)
        return self

    def stack_x(self, first_position='left', x=0):
        'Arrange objects such that the form a stack in the x-direction.'
        x_pos = x
        for idx, i in enumerate(self.shapes):
            if idx == 0:
                i.align_x(first_position, x_pos)
            else:
                i.align_x('left', x_pos)
            x_pos = i.x_max

        return self

    def stack_y(self, first_position='top', y=0):
        'Arrange objects such that the form a stack in the y-direction.'
        y_pos = y
        for idx, i in enumerate(self.shapes):
            if idx == 0:
                i.align_y(first_position, y_pos)
            else:
                i.align_y('top', y_pos)
            y_pos = i.y_min
        return self

    def group_align_x(self, position='centre', x=0):
        'Align all objects together to a given x-coordinate.'
        if position == 'left':
            shift = x - self.x_min
        elif position == 'centre':
            shift = x - self.x_mid
        elif position == 'right':
            shift = x - self.x_max

        for i in self.shapes:
            i.translate(shift, 0)

        self._update_centroid()

        return self

    def group_align_y(self, position='middle', y=0):
        'Align all objects together to a given y-coordinate.'

        if position == 'bottom':
            shift = y - self.y_min
        elif position == 'middle':
            shift = y - self.y_mid
        elif position == 'top':
            shift = y - self.y_max

        for i in self.shapes:
            i.translate(0, shift)

        self._update_centroid()

        return self

    def get_first_area_moment(self, axis):
        M = 0
        for i in self.shapes:
            M += (i.area_sign * i.get_first_area_moment(axis))
        return M

    def get_second_area_moment(self, axis):
        I = 0
        for i in self.shapes:
            I += (i.area_sign * i.get_second_area_moment(axis))
        return I

    def get_centroid(self, x=0, y=0):
        'Get centroid relative to a given position.'
        # Set up Axis objects:
        x_axis = XAxis(y=y)
        y_axis = YAxis(x=x)

        cx = self.get_first_area_moment(y_axis) / self.area
        cy = self.get_first_area_moment(x_axis) / self.area

        return cx, cy

    def get_centroidal_xaxis(self):
        cent = self.get_centroid()
        xaxis = XAxis(y=cent[1])
        return xaxis

    def get_centroidal_yaxis(self):
        cent = self.get_centroid()
        yaxis = YAxis(x=cent[0])
        return yaxis

    def get_max_bending_stress(self, max_bending_moment):
        xaxis = self.get_centroidal_xaxis()
        I = self.get_second_area_moment(xaxis)
        ymax = xaxis.distance_from_point([0, self.y_max])
        return max_bending_moment * ymax / I

    def get_dimension_labels(self, figure_width, **kwargs):

        annots = []
        shapes = []

        overlap_x_idx = self.get_overlap_groups(self.overlap_x_idx)
        overlap_x_lo_idx = overlap_x_idx[:(len(overlap_x_idx) // 2)]
        overlap_x_hi_idx = overlap_x_idx[(len(overlap_x_idx) // 2):]
        # print('overlap_x_lo_idx: {}'.format(overlap_x_lo_idx))
        # print('overlap_x_hi_idx: {}'.format(overlap_x_hi_idx))

        overlap_y_idx = self.get_overlap_groups(self.overlap_y_idx)
        overlap_y_lo_idx = overlap_y_idx[:(len(overlap_y_idx) // 2)]
        overlap_y_hi_idx = overlap_y_idx[(len(overlap_y_idx) // 2):]
        # print('overlap_y_lo_idx: {}'.format(overlap_y_lo_idx))
        # print('overlap_y_hi_idx: {}'.format(overlap_y_hi_idx))

        # Units per pixel
        x_units_pp = (self.x_max - self.x_min) / figure_width
        y_units_pp = (self.y_max - self.y_min) / (
            figure_width * ((self.y_max - self.y_min) / (self.x_max - self.x_min))
        )

        for idx, i in enumerate(self.shapes):

            # Roughly in pixels, (not really...):
            width_offset_px = 40
            height_offset_px = 40
            width_add_offset_px = 100
            height_add_offset_px = width_add_offset_px

            width_offset = width_offset_px * x_units_pp
            height_offset = height_offset_px * y_units_pp
            width_add_offset = width_add_offset_px * x_units_pp
            height_add_offset = height_add_offset_px * y_units_pp

            x_lo_sub_idx = np.where([idx in i for i in overlap_x_lo_idx])[0]
            x_hi_sub_idx = np.where([idx in i for i in overlap_x_hi_idx])[0]
            if x_lo_sub_idx.size:
                # print('x_lo_sub_idx[0]: {}'.format(x_lo_sub_idx[0]))
                width_side = 'top'
                width_offset += (self.y_max - i.y_max) + \
                    width_add_offset * x_lo_sub_idx[0]

            else:
                # print('x_lo_hi_idx[0]: {}'.format(x_hi_sub_idx[0]))
                width_side = 'bottom'
                width_offset += (i.y_min - self.y_min) + \
                    width_add_offset * x_hi_sub_idx[0]

            y_lo_sub_idx = np.where([idx in i for i in overlap_y_lo_idx])[0]
            y_hi_sub_idx = np.where([idx in i for i in overlap_y_hi_idx])[0]
            if any([idx in i for i in overlap_y_lo_idx]):
                height_side = 'right'
                height_offset += (self.x_max - i.x_max) + \
                    height_add_offset * y_lo_sub_idx[0]
            else:
                height_side = 'left'
                height_offset += (i.x_min - self.x_min) + \
                    height_add_offset * y_hi_sub_idx[0]

            # print('width_offset: {}'.format(width_offset))
            # print('height_offset: {}'.format(height_offset))

            annots_i, shapes_i = i.get_dimension_labels(
                width_offset=width_offset,
                height_offset=height_offset,
                width_side=width_side,
                height_side=height_side,
                **kwargs
            )
            annots.extend(annots_i)
            shapes.extend(shapes_i)

        return annots, shapes


class XAxis(object):

    def __init__(self, y=0, name=None):

        self.y = y
        self.name = name

    def __repr__(self):
        out = (
            '{}('
            'y={}'
            ')'
        ).format(
            self.__class__.__name__,
            self.y,
        )
        return out

    def distance_from_point(self, point):
        return point[1] - self.y

    def distance_from_axis(self, axis):
        if isinstance(axis, XAxis):
            point = [0, axis.y]
            return self.distance_from_point(point)
        else:
            raise ValueError('Bad axis.')

    def get_plot_shape(self):
        out = {
            'type': 'line',
            'x0': 0,
            'x1': 1,
            'xref': 'paper',
            'y0': self.y,
            'y1': self.y,
            'yref': 'y',
            'line': {
                'width': 1.5,
            },
        }
        return out


class YAxis(object):

    def __init__(self, x=0, name=None):

        self.x = x
        self.name = name

    def __repr__(self):
        out = (
            '{}('
            'x={}'
            ')'
        ).format(
            self.__class__.__name__,
            self.x,
        )
        return out

    def distance_from_point(self, point):
        return point[0] - self.x

    def distance_from_axis(self, axis):
        if isinstance(axis, YAxis):
            point = [axis.x, 0]
            return self.distance_from_point(point)
        else:
            raise ValueError('Bad axis.')

    def get_plot_shape(self):
        out = {
            'type': 'line',
            'x0': self.x,
            'x1': self.x,
            'xref': 'x',
            'y0': 0,
            'y1': 1,
            'yref': 'paper',
            'line': {
                'width': 1.5,
            },
        }
        return out
