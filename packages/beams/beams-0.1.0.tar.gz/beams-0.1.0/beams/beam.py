'`beams.beam.py`'

import numbers

import numpy as np
from ipywidgets import widgets
from plotly import graph_objects as go
from plotly.colors import DEFAULT_PLOTLY_COLORS

from beams.shapes import Shape, CrossSection
from beams.utils import rgb_to_rgba, get_circle_trace, get_plotly_arrow_shapes


def deflection_point_load_cantilever(x, flexural_rigidity, load, length):
    out = (1 / flexural_rigidity) * (
        - (load * (x ** 3)) / 6
        + (load * x * (length ** 2)) / 2
        - (load * (length ** 3)) / 3
    )
    return out


def deflection_point_load_simply_supported(x, flexural_rigidity, load, length):
    raise NotImplementedError()


def deflection_ud_load_cantilever(x, flexural_rigidity, load, length):
    raise NotImplementedError()


def deflection_ud_load_simply_supported(x, flexural_rigidity, load, length):
    out = (1 / flexural_rigidity) * (
        + (load * length * (x ** 3)) / 12
        - (load * (x ** 4)) / 24
        - (load * x * (length ** 3)) / 24
    )
    return out


def slope_point_load_cantilever(x, flexural_rigidity, load, length):
    out = (1 / flexural_rigidity) * (
        - (load * (x ** 2)) / 2
        + (load * (length ** 2)) / 2
    )
    return out


def slope_point_load_simply_supported(x, flexural_rigidity, load, length):
    raise NotImplementedError()


def slope_ud_load_cantilever(x, flexural_rigidity, load, length):
    raise NotImplementedError()


def slope_ud_load_simply_supported(x, flexural_rigidity, load, length):
    out = (1 / flexural_rigidity) * (
        + (load * length * (x **2)) / 4
        - (load * (x ** 3)) / 3
        - (load * (length ** 3)) / 24
    )
    return out


deflection_funcs={
    'point_load_cantilever': deflection_point_load_cantilever,
    'point_load_simply_supported': deflection_point_load_simply_supported,
    'udl_cantilever': deflection_ud_load_cantilever,
    'udl_simply_supported': deflection_ud_load_simply_supported,


}
slope_funcs = {
    'point_load_cantilever': slope_point_load_cantilever,
    'point_load_simply_supported': slope_point_load_simply_supported,
    'udl_cantilever': slope_ud_load_cantilever,
    'udl_simply_supported': slope_ud_load_simply_supported,
}


class BeamLoad(object):

    def _get_moment(self, x=0):
        'Get the moment of the load from a given position.'

        dist = x - self.effective_point_load.distance
        out = self.effective_point_load.load * dist
        # print('BeamLoad.get_moment: dist: {} mom: {}'.format(dist, out))
        return out

    @property
    def effective_point_load(self):
        # overrode by DistributedLoad
        return self


class PointLoad(BeamLoad):

    def __init__(self, load, distance):
        self.load = load
        self.distance = distance

    def __repr__(self):
        out = (
            '{}('
            'load={!r}, '
            'distance={!r}'
            ')'
        ).format(
            self.__class__.__name__,
            self.load,
            self.distance,
        )
        return out

    def get_shear_force_contribution(self, x):
        if x < self.distance:
            return 0
        else:
            return self.load

    def get_left_moment(self, x):
        if self.distance < x:
            return self._get_moment(x)
        else:
            return 0


class DistributedLoad(BeamLoad):

    def __init__(self, load, distance_start, distance_end):
        if distance_end <= distance_start:
            raise ValueError('Bad distance_start/distance_end')
        self.load = load
        self.distance_start = distance_start
        self.distance_end = distance_end

    def __repr__(self):
        out = (
            '{}('
            'load={!r}, '
            'distance_start={!r}, '
            'distance_end={!r}'
            ')'
        ).format(
            self.__class__.__name__,
            self.load,
            self.distance_start,
            self.distance_end,
        )
        return out

    @property
    def load_width(self):
        return self.distance_end - self.distance_start

    @property
    def effective_point_load(self):
        load = self.load_width * self.load
        distance = (self.distance_start + self.distance_end) / 2
        return PointLoad(load, distance)

    def get_shear_force_contribution(self, x):
        if x < self.distance_start:
            return 0
        elif x > self.distance_end:
            return self.load_width * self.load
        else:
            return (x - self.distance_start) * self.load

    def get_left_moment(self, x):
        if self.distance_start >= x:
            return 0
        elif self.distance_end <= x:
            eff_point_load = self.effective_point_load
        else:
            new_end = x
            load_width = new_end - self.distance_start
            load = load_width * self.load
            midpoint = (self.distance_start + new_end) / 2
            eff_point_load = PointLoad(load, midpoint)

        return eff_point_load._get_moment(x)


class BeamSupport(object):

    def __init__(self, position, support_type='simple'):
        self.position = position
        self.support_type = support_type
        self.force = None

    def __repr__(self):
        out = (
            '{}('
            'position={!r}, '
            'support_type={!r}'
            ')'
        ).format(
            self.__class__.__name__,
            self.position,
            self.support_type,
        )
        return out

    def get_shear_force_contribution(self, x):
        if x < self.position:
            return 0
        else:
            return self.force

    def get_left_moment(self, x):
        if self.position < x:
            dist = x - self.position
            return self.force * dist
        else:
            return 0


class Beam(object):

    FIG_FONT_SIZE = 15
    FIG_FONT = 'Courier'
    FIG_FIXED_SUPPORT_COLOUR = 'rgb(90, 90, 90)'
    FIG_BEAM_OUTLINE_COLOUR = FIG_FIXED_SUPPORT_COLOUR
    FIG_BEAM_FILL_COLOUR = 'silver'
    FIG_DIMENSION_LABEL_LINE = {
        'width': 1.5,
        'color': 'gray',
        'dash': 'dot',
    }
    UNITS_LENGTH = 'm'
    UNITS_FORCE = 'N'

    def __init__(self, width, supports, loads=None, cross_section=None, height_ratio=0.1,
                 units=None, figure_width=700, cross_section_centroids=True,
                 flexural_rigidity=None, elastic_modulus=None):

        self.width = width
        self.height_ratio = height_ratio
        self.supports = self._validate_supports(supports)
        self.loads = loads or []

        self._flexural_rigidity = flexural_rigidity
        self._elastic_modulus = elastic_modulus

        if not units:
            units = {
                'length': Beam.UNITS_LENGTH,
                'force': Beam.UNITS_FORCE,
            }
        self.units = units

        self.figure_width = figure_width
        self.cross_section_centroids = cross_section_centroids

        self._fig_shapes_idx = {}
        self._fig_annots_idx = {}

        self.figures = {
            'beam': self._get_beam_figure(),
            'cross_section': self._init_cross_section_figure(),
        }

        self.cross_section = cross_section

        self._supports_solved = False

        self._visual = None
        self._visual_shear_force = None
        self._visual_bending_moment = None

    def __repr__(self):
        out = (
            '{}('
            'width={!r}, '
            'supports={!r}, '
            'loads={!r}, '
            'cross_section={!r}'
            ')'
        ).format(
            self.__class__.__name__,
            self.width,
            self.supports,
            self.loads,
            self.cross_section,
        )
        return out

    @property
    def flexural_rigidity(self):
        if self._flexural_rigidity is not None:
            return self._flexural_rigidity
        else:
            if self.cross_section is None:
                msg = 'Flexural rigidity nor cross-section specified.'
                raise ValueError(msg)
            elif self._elastic_modulus is None:
                msg = 'Flexural rigidity nor elastic modulus specified.'
                raise ValueError(msg)
            else:
                axis = self.cross_section.get_centroidal_xaxis()
                I = self.cross_section.get_second_area_moment(axis)
                EI = I * self._elastic_modulus
                return EI

    @property
    def has_positive_loads(self):
        'Is the beam loaded from the bottom at all?'
        for i in self.loads:
            if i.load > 0:
                return True
        return False

    @property
    def point_loads(self):
        return [i for i in self.loads if isinstance(i, PointLoad)]

    @property
    def distributed_loads(self):
        return [i for i in self.loads if isinstance(i, DistributedLoad)]

    @property
    def cross_section(self):
        return self._cross_section

    @cross_section.setter
    def cross_section(self, cross_section):
        if cross_section is None:
            self._cross_section = cross_section
            return

        if False:
            if not isinstance(cross_section, (Shape, CrossSection)):
                msg = '`cross_section` must be a `Shape` or `CrossSection`.'
                raise ValueError(msg)

        self._cross_section = cross_section
        for i in self._cross_section._get_plot_traces(self.cross_section_centroids):
            self.figures['cross_section'].add_trace(i)

        dim_annots, dim_shapes = cross_section.get_dimension_labels(
            line_props=Beam.FIG_DIMENSION_LABEL_LINE,
            font={'family': Beam.FIG_FONT, 'size': Beam.FIG_FONT_SIZE},
            figure_width=(self.figure_width / 2),
        )

        old_annots = list(self.figures['cross_section'].layout.annotations)
        self.figures['cross_section'].layout.annotations = old_annots + dim_annots

        old_shapes = list(self.figures['cross_section'].layout.shapes)
        self.figures['cross_section'].layout.shapes = old_shapes + dim_shapes

    @property
    def _height(self):
        return self.width * self.height_ratio

    def _validate_supports(self, supports):

        # Check at least two supports (one of which can be `None`:
        if len(supports) != 2:
            raise ValueError('Must be two "support"s (but one can be `None`).')

        # Check not all supports are None
        if all([i is None for i in supports]):
            raise ValueError('All supports cannot be `None`!')

        objs = []
        for idx, support in enumerate(supports):
            if support == 'fixed':
                # Check fixed support is the first or last support:
                if idx not in [0, len(supports) - 1]:
                    raise ValueError('Fixed support must be first or last support.')
                sup_obj = BeamSupport(
                    position=(0 if idx == 0 else self.width), support_type='fixed')
            elif support is None:
                sup_obj = None
            elif isinstance(support, numbers.Number):
                sup_obj = BeamSupport(position=support, support_type='simple')
            else:
                raise ValueError('Bad support spec.')
            objs.append(sup_obj)

        return objs

    def _get_plot_traces(self):

        annots = []  # Annotations for simple support x-coordinates
        data = [
            # Beam itself:
            {
                'type': 'scatter',
                'mode': 'lines',
                'x': [0, self.width, self.width, 0, 0],
                'y': [-self._height / 2, -self._height / 2, self._height / 2, self._height / 2, -self._height / 2],
                'fill': 'toself',
                # 'fillcolor': rgb_to_rgba(DEFAULT_PLOTLY_COLORS[0], 0.5),
                'fillcolor': Beam.FIG_BEAM_FILL_COLOUR,
                'name': 'Beam',
                'line': {
                    'color': Beam.FIG_BEAM_OUTLINE_COLOUR,
                }
            },
        ]

        # Add supports:
        for idx, support in enumerate(self.supports):
            if support is None:
                continue
            if support.support_type == 'fixed':
                fixed_sup_height = self._height * 2
                fixed_sup_width = fixed_sup_height * 0.1
                fixed_sup_dat = {
                    'type': 'scatter',
                    'mode': 'lines',
                    'y': [
                        -fixed_sup_height / 2,
                        -fixed_sup_height / 2,
                        fixed_sup_height / 2,
                        fixed_sup_height / 2,
                        -fixed_sup_height / 2,
                    ],
                    'fill': 'toself',
                    'fillcolor': Beam.FIG_FIXED_SUPPORT_COLOUR,
                    'line': {
                        'color': Beam.FIG_FIXED_SUPPORT_COLOUR,
                    },
                    'name': 'Fixed support',
                }
                if idx == 0:
                    # left end is fixed
                    fixed_sup_dat['x'] = [
                        -fixed_sup_width,
                        0,
                        0,
                        -fixed_sup_width,
                        -fixed_sup_width,
                    ]
                elif idx == len(self.supports) - 1:
                    # right end is fixed
                    fixed_sup_dat['x'] = [
                        self.width,
                        self.width + fixed_sup_width,
                        self.width + fixed_sup_width,
                        self.width,
                        self.width,
                    ]
                data.append(fixed_sup_dat)

            elif isinstance(support, BeamSupport):
                # simple support
                radius = self._height * 0.2
                origin = [support.position, -self._height / 2 - radius]
                circ_trace = get_circle_trace(radius, origin)
                circ_trace.update({
                    'fill': 'toself',
                    'fillcolor': rgb_to_rgba(DEFAULT_PLOTLY_COLORS[1], 0.5),
                    'line': {
                        'color': rgb_to_rgba(DEFAULT_PLOTLY_COLORS[1], 0.5),
                    },
                    'name': 'Simple support'
                })
                data.append(circ_trace)

                annots.append({
                    'x': support.position,
                    'y': -self._height * 1.2,
                    'text': 'x={:.1f}'.format(support.position),
                    'showarrow': False,
                    'font': {
                        'size': Beam.FIG_FONT_SIZE,
                        'family': Beam.FIG_FONT,
                    },
                })

        return data, annots

    def _get_load_arrows(self):

        arrow_width_point = self.figure_width * 0.02
        arrow_width_dist = arrow_width_point * 0.7
        dist_line_width = 1.5

        point_load_length = self._height * 1.2
        dist_load_length = self._height * 0.8
        # print('point_load_length: {}'.format(point_load_length))
        # print('dist_load_length: {}'.format(dist_load_length))

        load_text_y_point = 1.5 * point_load_length
        load_text_y_dist = 1.8 * dist_load_length
        # print('load_text_y_point: {}'.format(load_text_y_point))
        # print('load_text_y_dist: {}'.format(load_text_y_dist))

        annots = []
        shapes = []
        for i in self.point_loads:
            load_sign_factor = -i.load / abs(i.load)
            point = [i.distance, load_sign_factor * (self._height / 2)]

            is_down = not bool(load_sign_factor - 1)

            shapes.extend(
                get_plotly_arrow_shapes(
                    point=point,
                    width=arrow_width_point,
                    length=point_load_length,
                    line_width=2,
                    down=is_down,
                )
            )

            # Add text:
            annots.append({
                'x': i.distance,
                'y': load_sign_factor * load_text_y_point,
                'showarrow': False,
                'xref': 'x',
                'yref': 'y',
                'yanchor': 'bottom' if is_down else 'top',
                'text': '<b>{} {}</b><br>x={:.1f}'.format(
                    i.load, self.units['force'], i.distance).replace('-', '−'),
                'font': {
                    'size': Beam.FIG_FONT_SIZE,
                    'family': Beam.FIG_FONT,
                },
            })

        for i in self.distributed_loads:
            load_sign_factor = -i.load / abs(i.load)
            is_down = not bool(load_sign_factor - 1)
            load_width = i.distance_end - i.distance_start
            shapes.append({
                'type': 'line',
                'x0': i.distance_start,
                'x1': i.distance_end,
                'y0': load_sign_factor * dist_load_length + (self._height / 2),
                'y1': load_sign_factor * dist_load_length + (self._height / 2),
                'line': {
                    'width': dist_line_width,
                },
            })
            N0 = load_width / (self.width * 0.1)
            N = int(N0)
            interval_size = load_width / (N + 1)
            for n in range(N + 1):

                point = [
                    i.distance_start + n * interval_size,
                    load_sign_factor * (self._height / 2),
                ]

                shapes.extend(
                    get_plotly_arrow_shapes(
                        point=point,
                        width=arrow_width_dist,
                        length=dist_load_length,
                        line_width=dist_line_width,
                        down=is_down,
                    )
                )

            # Add one to the end:
            point = [
                i.distance_end,
                load_sign_factor * (self._height / 2),
            ]
            shapes.extend(
                get_plotly_arrow_shapes(
                    point=point,
                    width=arrow_width_dist,
                    length=dist_load_length,
                    line_width=dist_line_width,
                    down=is_down,
                )
            )

            # Add text
            annots.append({
                'x': i.distance_start + (load_width / 2),
                'y': load_sign_factor * load_text_y_dist,
                'xref': 'x',
                'yref': 'y',
                'yanchor': 'bottom',
                'showarrow': False,
                'text': '<b>{} {}/{}</b><br>x=[{:.1f},{:.1f}]'.format(
                    i.load,
                    self.units['force'],
                    self.units['length'],
                    i.distance_start,
                    i.distance_end,
                ).replace('-', '−'),
                'font': {
                    'size': 15,
                    'family': Beam.FIG_FONT,
                },
            })

        return annots, shapes

    def _get_figure_labels(self):

        annots = []
        shapes = []

        length_lab_y = -self._height * 1.5
        length_lab_text_y = length_lab_y * 1.3
        if self.has_positive_loads:
            length_lab_y *= 2.2
            length_lab_text_y *= 1.9

        length_label = [
            {
                'type': 'line',
                'x0': 0,
                'y0': length_lab_y,
                'x1': self.width,
                'y1': length_lab_y,
                'line': Beam.FIG_DIMENSION_LABEL_LINE,
            },
            {
                'type': 'line',
                'x0': 0,
                'y0': -10,
                'yanchor': length_lab_y,
                'ysizemode': 'pixel',
                'x1': 0,
                'y1': 10,
                'line': Beam.FIG_DIMENSION_LABEL_LINE,
            },
            {
                'type': 'line',
                'x0': self.width,
                'y0': -10,
                'yanchor': length_lab_y,
                'ysizemode': 'pixel',
                'x1': self.width,
                'y1': 10,
                'line': Beam.FIG_DIMENSION_LABEL_LINE,
            },
        ]
        shapes.extend(length_label)
        annots.append({
            'text': 'L = {:.1f} {}'.format(self.width, self.units['length']),
            'x': (self.width / 2),
            'xanchor': 'center',
            'y': length_lab_text_y,
            'yanchor': 'top',
            'showarrow': False,
            'font': {
                'size': Beam.FIG_FONT_SIZE,
                'family': Beam.FIG_FONT,
            },
        })

        return annots, shapes

    def _get_beam_figure(self):
        'Get Plotly FigureWidget of the beam.'

        data, support_annots = self._get_plot_traces()
        pad = self.width * 0.18
        load_annots, load_shapes = self._get_load_arrows()
        labs_annots, labs_shapes = self._get_figure_labels()

        length_label_annots_idx = list(range(
            len(load_annots), len(load_annots) + len(labs_annots)))
        length_label_shapes_idx = list(range(
            len(load_shapes), len(load_shapes) + len(labs_shapes)))

        support_annots_idx = list(range(
            length_label_annots_idx[-1] + 1, length_label_annots_idx[-1] + 1 + len(support_annots)))

        # print('dimension_label_annots_idx: {}'.format(length_label_annots_idx))
        # print('dimension_label_shapes_idx: {}'.format(length_label_shapes_idx))
        # print('support_annots_idx: {}'.format(support_annots_idx))

        self._fig_shapes_idx.update({'length_label': length_label_shapes_idx})
        self._fig_annots_idx.update({
            'length_label': length_label_annots_idx,
            'support_labels': support_annots_idx,
        })

        layout = {
            'template': 'none',
            'showlegend': False,
            'xaxis': {
                'scaleanchor': 'y',
                # 'fixedrange': True,
                'showticklabels': False,
                'zeroline': False,
                'range': [-pad, self.width + pad],
                'showgrid': False,
            },
            'yaxis': {
                # 'fixedrange': True,
                'zeroline': False,
                'showticklabels': False,
                'showgrid': False,
            },
            'annotations': load_annots + labs_annots + support_annots,
            'shapes': load_shapes + labs_shapes,
            'width': self.figure_width,
            'margin': {
                't': 0,
                'r': 0,
                'b': 0,
                'l': 0,
            },
        }
        fig = go.FigureWidget(data=data, layout=layout)

        return fig

    def _init_cross_section_figure(self):
        data = []
        layout = {
            'showlegend': False,
            'template': 'none',
            'margin': {
                't': 0,
                'r': 0,
                'b': 0,
                'l': 30,
            },
            'width': self.figure_width / 2,
            'xaxis': {
                'scaleanchor': 'y',
                'showticklabels': False,
                'zeroline': False,
                'showgrid': False,
            },
            'yaxis': {
                'showticklabels': False,
                'zeroline': False,
                'showgrid': False,
            },
        }
        fig = go.FigureWidget(data=data, layout=layout)
        return fig

    def _make_visual(self):
        out = widgets.HBox(
            children=[
                self.figures['beam'],
                self.figures['cross_section'],
            ]
        )
        return out

    def show(self):
        if self._visual is None:
            self._visual = self._make_visual()
        return self._visual

    def get_deflection_type(self):
        """
        Returns
        -------
        str
            One of:
                "point_load_cantilever"
                "point_load_simply_supported",
                "udl_cantilever"
                "udl_simply_supported"
        """

        if len(self.loads) == 0:
            msg = 'Deflection cannot be computed for no loads!'
            raise ValueError(msg)

        elif len(self.loads) > 1:
            msg = 'Deflection cannot be computed for more than one load.'
            raise NotImplementedError(msg)

        sup_idx = [idx for idx, i in enumerate([j is not None for j in self.supports])
                   if i is True]

        if len(sup_idx) == 1:
            # Check cantilever:
            if self.supports[sup_idx[0]].support_type != 'fixed':
                msg = ('Deflection cannot be computed.')
                raise NotImplementedError(msg)
        elif len(sup_idx) == 2:
            # Check simply supported:
            if not all([i.support_type == 'simple' for i in self.supports]):
                msg = ('Deflection cannot be computed for multiple non-simple '
                       'supports.')
                raise NotImplementedError(msg)
        else:
            raise NotImplementedError('Deflection cannot be computed.')

        if self.point_loads:

            point_load = self.point_loads[0]

            if len(sup_idx) == 1:
                # Check load is at the free end if cantilever:
                if sup_idx[0] == 0:
                    free_end_x = self.width
                elif sup_idx[0] == 1:
                    free_end_x = 0

                if point_load.distance != free_end_x:
                    msg = 'Deflection cannot be computed.'
                    raise NotImplementedError(msg)

                return 'point_load_cantilever'

            if len(sup_idx) == 2:
                # Check load is in middle if simply-supported:
                if point_load.distance != (self.width / 2):
                    msg = ('Deflection cannot be computed for a point load that is not '
                           'located at the centre of the beam.')
                    raise NotImplementedError(msg)

                return 'point_load_simply_supported'

        elif self.distributed_loads:

            dist_load = self.distributed_loads[0]

            # Check UDL is across the whole beam:
            if dist_load.distance_start != 0 or dist_load.distance_end != self.width:
                msg = ('Deflection cannot be computed for a UDL that does not space the '
                       'entirety of the beam.')
                raise NotImplementedError(msg)

            if len(sup_idx) == 1:
                return 'udl_cantilever'

            if len(sup_idx) == 2:
                return 'udl_simply_supported'

    @property
    def deflection_func(self):
        def_type = self.get_deflection_type()
        return deflection_funcs[def_type]

    @property
    def slope_func(self):
        def_type = self.get_deflection_type()
        return slope_funcs[def_type]

    @property
    def total_load(self):
        load = 0
        for i in self.point_loads:
            load += i.load
        for i in self.distributed_loads:
            load += i.effective_point_load.load

        return -load

    @property
    def supports_solved(self):
        return self._supports_solved

    def solve_supports(self):
        'Find reaction forces on supports'

        if self.supports_solved:
            msg = 'Supports are already solved.'
            raise ValueError(msg)
        else:
            self._supports_solved = True

        if len(self.supports) > 2:
            raise NotImplementedError

        # Take moment about first support:
        moment = 0
        moment_centre = self.supports[0].position
        for i in self.point_loads + self.distributed_loads:
            moment += i._get_moment(moment_centre)

        r2 = moment / (self.supports[1].position - moment_centre)
        r1 = self.total_load - r2

        self.supports[0].force = r1
        self.supports[1].force = r2

        beam_fig = self.figures['beam']
        shapes = []
        annots = []

        point_load_length = self._height * 1.2
        load_text_y_point = -1.5 * point_load_length
        arrow_width_point = self.figure_width * 0.02

        point = [
            self.supports[0].position,
            -self._height / 2,
        ]
        shapes.extend(
            get_plotly_arrow_shapes(
                point=point,
                width=arrow_width_point,
                length=point_load_length,
                line_width=2,
                down=False,
            )
        )

        point = [
            self.supports[1].position,
            -self._height / 2,
        ]
        shapes.extend(
            get_plotly_arrow_shapes(
                point=point,
                width=arrow_width_point,
                length=point_load_length,
                line_width=2,
                down=False,
            )
        )

        # Add text:
        for i in [0, 1]:
            annots.append(
                {
                    'x': self.supports[i].position,
                    'y': load_text_y_point,
                    'showarrow': False,
                    'xref': 'x',
                    'yref': 'y',
                    'yanchor': 'top',
                    'text': '<b>{} {}</b><br>x={:.1f}'.format(
                        self.supports[i].force,
                        self.units['force'],
                        self.supports[i].position
                    ).replace('-', '−'),
                    'font': {
                        'size': Beam.FIG_FONT_SIZE,
                        'family': Beam.FIG_FONT,
                    },
                }
            )

        old_annots = list(beam_fig.layout['annotations'])
        beam_fig.layout['annotations'] = old_annots + annots

        old_shapes = list(beam_fig.layout['shapes'])
        beam_fig.layout['shapes'] = old_shapes + shapes

        # Shift beam length label down:
        beam_fig.layout.annotations[self._fig_annots_idx['length_label'][0]].y *= 1.9
        beam_fig.layout.shapes[self._fig_shapes_idx['length_label'][0]].y0 *= 2.2
        beam_fig.layout.shapes[self._fig_shapes_idx['length_label'][0]].y1 *= 2.2
        beam_fig.layout.shapes[self._fig_shapes_idx['length_label'][1]].yanchor *= 2.2
        beam_fig.layout.shapes[self._fig_shapes_idx['length_label'][2]].yanchor *= 2.2

        # Remove previous support labels:
        beam_fig.layout.annotations[self._fig_annots_idx['support_labels'][0]].text = ''
        beam_fig.layout.annotations[self._fig_annots_idx['support_labels'][1]].text = ''

    def get_shear_force(self, x):

        shear_force = 0
        for i in self.distributed_loads:
            shear_force += i.get_shear_force_contribution(x)

        for i in self.point_loads:
            shear_force += i.get_shear_force_contribution(x)

        if self.supports[0] and self.supports[0].force is None:
            self.solve_supports()
        for i in self.supports:
            if i is not None:
                if i.support_type == 'simple':
                    shear_force += i.get_shear_force_contribution(x)

        return shear_force

    def get_moment(self, x):

        moment = 0
        for i in self.point_loads:
            moment += i.get_left_moment(x)

        for i in self.distributed_loads:
            moment += i.get_left_moment(x)

        if self.supports[0] and self.supports[0].force is None:
            self.solve_supports()
        for i in self.supports:
            if i is not None:
                if i.support_type == 'simple':
                    moment += i.get_left_moment(x)

        return moment

    def get_deflection(self, x):
        y = self.deflection_func(x, self.flexural_rigidity,
                                 np.abs(self.loads[0].load), self.width)
        return y

    def get_slope(self, x):
        y = self.slope_func(x, self.flexural_rigidity,
                            np.abs(self.loads[0].load), self.width)
        return y

    def _get_deflection_plot_data(self):
        x = np.linspace(0, self.width, num=100)
        y = self.get_deflection(x)
        data = [
            {
                'type': 'scatter',
                'mode': 'lines',
                'x': x,
                'y': y,
            }
        ]
        return data

    def _get_slope_data_plot(self):
        x = np.linspace(0, self.width, num=100)
        y = self.get_slope(x)
        data = [
            {
                'type': 'scatter',
                'mode': 'lines',
                'x': x,
                'y': y,
            }
        ]
        return data

    def _get_shear_force_plot_data(self):

        x = np.linspace(0, self.width, num=100)
        y = []
        for i in x:
            y.append(self.get_shear_force(i))
        y = np.array(y)

        # Add more points at the discontinuities:
        new_x = []
        new_y = []
        for i in self.point_loads:
            new_x.extend([i.distance - 1e-8, i.distance])
            new_y.extend([
                self.get_shear_force(i.distance - 1e-8),
                self.get_shear_force(i.distance),
            ])

        for i in self.supports:
            if i is not None and i.support_type == 'simple':
                new_x.extend([i.position - 1e-8, i.position])
                new_y.extend([
                    self.get_shear_force(i.position - 1e-8),
                    self.get_shear_force(i.position),
                ])

        x = np.concatenate([x, new_x])
        y = np.concatenate([y, new_y])

        x_srt = np.argsort(x)
        x = x[x_srt]
        y = y[x_srt]

        data = [
            {
                'type': 'scatter',
                'mode': 'lines',
                'x': x,
                'y': y,
            }
        ]
        return data

    def _get_bending_moment_plot_data(self):

        x = np.linspace(0, self.width, num=100)
        y = []
        for i in x:
            y.append(self.get_moment(i))
        data = [
            {
                'type': 'scatter',
                'mode': 'lines',
                'x': x,
                'y': y,
            }
        ]
        return data

    def show_shear_force(self):

        data = self._get_shear_force_plot_data()
        pad = self.width * 0.1
        layout = {
            'width': self.figure_width,
            'title': 'Shear force diagram',
            'xaxis': {
                'range': [-pad, self.width + pad],
                'title': 'x /{}'.format(self.units['length']),
            },
            'yaxis': {
                'title': 'Shear force /{}'.format(self.units['force']),
            }
        }
        fig = go.FigureWidget(data=data, layout=layout)
        self.visual_shear_force = fig

        return fig

    def show_bending_moment(self):

        data = self._get_bending_moment_plot_data()
        pad = self.width * 0.1
        layout = {
            'width': self.figure_width,
            'title': 'Bending moment diagram',
            'xaxis': {
                'range': [-pad, self.width + pad],
                'title': 'x /{}'.format(self.units['length']),
            },
            'yaxis': {
                'title': 'Bending moment /{}{}'.format(self.units['force'], self.units['length']),
            }
        }
        fig = go.FigureWidget(data=data, layout=layout)

        return fig

    def show_deflection(self):

        data = self._get_deflection_plot_data()
        pad = self.width * 0.1
        layout = {
            'width': self.figure_width,
            'title': 'Deflection',
            'xaxis': {
                'range': [-pad, self.width + pad],
                'title': 'x /{}'.format(self.units['length']),
            },
            'yaxis': {
                'title': 'Deflection /{}'.format(self.units['length']),
            }
        }
        fig = go.FigureWidget(data=data, layout=layout)

        return fig

    def show_slope(self):

        data = self._get_slope_data_plot()
        pad = self.width * 0.1
        layout = {
            'width': self.figure_width,
            'title': 'Slope',
            'xaxis': {
                'range': [-pad, self.width + pad],
                'title': 'x /{}'.format(self.units['length']),
            },
            'yaxis': {
                'title': 'Slope',
            }
        }
        fig = go.FigureWidget(data=data, layout=layout)

        return fig
