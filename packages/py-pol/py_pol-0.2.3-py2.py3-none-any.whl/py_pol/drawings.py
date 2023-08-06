# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------
# Authors:    Luis Miguel Sanchez Brea and Jesus del Hoyo
# Date:       2019/02/03 (version 1.0)
# License:    GPL
# ------------------------------------
""" functions for drawing """

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import (array, asarray, cos, exp, linspace, matrix, meshgrid,
                   ndarray, ones, outer, real, remainder, sin, size, sqrt,
                   zeros_like, mean)
from scipy.signal import fftconvolve

from . import degrees, eps
from .utils import nearest2

# print(matplotlib.__version__)

Axes3D = Axes3D  # pycharm auto import


def draw2D(image, x, y, color="hot"):  # YlGnBu  RdBu, jet, hot
    """Draws a 2D image.

    Parameters:
        x (numpy.array): x
        y (numpy.array): y
        xlabel (str): string for x label
        ylabel (str): string for y label
        title (str): title
        color (str): color
    """

    id_fig = plt.figure()
    IDax = id_fig.add_subplot(111)

    IDimage = plt.imshow(
        image,
        interpolation='bilinear',
        aspect='auto',
        origin='lower',
        extent=[x.min(), x.max(), y.min(), y.max()])

    plt.colorbar()
    IDimage.set_cmap(color)
    return id_fig, IDax, IDimage


def draw_poincare_sphere(stokes_points=None,
                         angle_view=[0.5, -1],
                         is_normalized=True,
                         kind='line',
                         color='r',
                         label='',
                         filename=''):
    """Function to draw the poincare sphere.
    It admits Stokes or a list with Stokes, or None

    Parameters:
        stokes_points (Stokes, list, None): list of Stokes points.
        angle_view (float, float): Elevation and azimuth for viewing.
        is_normalized (bool): normalize intensity to 1.
        kind (str): 'line' or 'scatter'.
        color (str): color of line or scatter.
        label (str): labels for drawing.
        filename (str): name of filename to save the figure.
    """

    elev, azim = angle_view
    max_size = 1

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d', adjustable='box')
    # ax.set_aspect('equal')

    u = linspace(0, 360 * degrees, 90)
    v = linspace(0, 180 * degrees, 90)

    x = 1 * outer(cos(u), sin(v))
    y = 1 * outer(sin(u), sin(v))
    z = 1 * outer(ones(size(u)), cos(v))

    ax.plot_surface(
        x,
        y,
        z,
        rstride=4,
        cstride=4,
        color='b',
        edgecolor="k",
        linewidth=.0,
        alpha=0.1)
    ax.plot(sin(u), cos(u), 0, color='k', linestyle='dashed', linewidth=0.5)
    ax.plot(
        sin(u),
        zeros_like(u),
        cos(u),
        color='k',
        linestyle='dashed',
        linewidth=0.5)
    ax.plot(
        zeros_like(u),
        sin(u),
        cos(u),
        color='k',
        linestyle='dashed',
        linewidth=0.5)

    ax.plot([-1, 1], [0, 0], [0, 0], 'k-.', lw=1, alpha=0.5)
    ax.plot([0, 0], [-1, 1], [0, 0], 'k-.', lw=1, alpha=0.5)
    ax.plot([0, 0], [0, 0], [-1, 1], 'k-.', lw=1, alpha=0.5)

    ax.plot(
        xs=(1, ),
        ys=(0, ),
        zs=(0, ),
        color='black',
        marker='o',
        markersize=4,
        alpha=0.5)

    ax.plot(
        xs=(-1, ),
        ys=(0, ),
        zs=(0, ),
        color='black',
        marker='o',
        markersize=4,
        alpha=0.5)
    ax.plot(
        xs=(0, ),
        ys=(1, ),
        zs=(0, ),
        color='black',
        marker='o',
        markersize=4,
        alpha=0.5)
    ax.plot(
        xs=(0, ),
        ys=(-1, ),
        zs=(0, ),
        color='black',
        marker='o',
        markersize=4,
        alpha=0.5)
    ax.plot(
        xs=(0, ),
        ys=(0, ),
        zs=(1, ),
        color='black',
        marker='o',
        markersize=4,
        alpha=0.5)
    ax.plot(
        xs=(0, ),
        ys=(0, ),
        zs=(-1, ),
        color='black',
        marker='o',
        markersize=4,
        alpha=0.5)
    distance = 1.2
    ax.text(distance, 0, 0, 'Q', fontsize=18)
    ax.text(0, distance, 0, 'U', fontsize=18)
    ax.text(0, 0, distance, 'V', fontsize=18)

    if stokes_points is not None:
        draw_on_poincare(
            ax,
            stokes_points,
            is_normalized=is_normalized,
            kind=kind,
            color=color,
            label=label)

    ax.view_init(elev=elev / degrees, azim=azim / degrees)

    ax.set_xlabel('$S_1$', fontsize=22)
    ax.set_ylabel('$S_2$', fontsize=22)
    ax.set_zlabel('$S_3$', fontsize=22)
    ax.grid(False)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    ax.set_xlim(-max_size, max_size)
    ax.set_ylim(-max_size, max_size)
    ax.set_zlim(-max_size, max_size)

    plt.tight_layout()
    set_aspect_equal_3d(ax)
    if filename not in (None, [], ''):
        plt.savefig(filename)
    return ax, fig


def draw_on_poincare(ax,
                     stokes_points,
                     is_normalized=True,
                     kind='line',
                     color='r',
                     label='',
                     filename=''):
    """Function to draw Stokes vectors on the poincare sphere.
    It admits Stokes or a list with Stokes,

    Parameters:
        stokes_points (Stokes, list, None): list of Stokes points.
        is_normalized (bool): normalize intensity to 1.
        kind (str): 'line' or 'scatter'.
        color (str): color of line or scatter.
        label (str): labels for drawing.
        filename (str): name of filename to save the figure.
    """

    if stokes_points is not None:
        if isinstance(stokes_points, list):
            if isinstance(stokes_points[0], matrix):
                stokes_points = asarray(stokes_points)
                s0 = stokes_points[:, 0].squeeze()
                s1 = stokes_points[:, 1].squeeze()
                s2 = stokes_points[:, 2].squeeze()
                s3 = stokes_points[:, 3].squeeze()
            else:
                points = []

                for i, point in enumerate(stokes_points):
                    points.append(point.M)

                stokes_points = asarray(points)
                s0 = array(stokes_points[:, 0]).squeeze()
                s1 = array(stokes_points[:, 1]).squeeze()
                s2 = array(stokes_points[:, 2]).squeeze()
                s3 = array(stokes_points[:, 3]).squeeze()
        elif isinstance(stokes_points, ndarray):
            s0 = array(stokes_points[:, 0]).squeeze()
            s1 = array(stokes_points[:, 1]).squeeze()
            s2 = array(stokes_points[:, 2]).squeeze()
            s3 = array(stokes_points[:, 3]).squeeze()
        else:
            s0 = array(stokes_points.M[0]).squeeze()
            s1 = array(stokes_points.M[1]).squeeze()
            s2 = array(stokes_points.M[2]).squeeze()
            s3 = array(stokes_points.M[3]).squeeze()

        if is_normalized is True:
            s1 = s1 / s0
            s2 = s2 / s0
            s3 = s3 / s0
            max_size = 1
        else:
            max_size = s0.max()

    if kind == 'line':
        ax.plot(s1, s2, s3, c=color, lw=2, label=label)
    elif kind == 'scatter':
        ax.scatter(s1, s2, s3, c=color, s=60, label=label)

    plt.tight_layout()
    if filename not in (None, [], ''):
        plt.savefig(filename)


def draw_ellipse_jones(j0, limit='', filename='', draw_arrow=False):
    """Draws polarization ellipse of Jones vector.

    Parameters:
        j0 (Jones_vector): Jones vector
        limit (float): limit for drawing. If empty itis obtained from ampltiudes.
        filename (str): name of filename to save the figure.
        draw_array (bool): draws chirality of ellipse

    Returns:
        fig (handle): handle to figure.
        ax (handle): handle to axis.
    """

    E_field = j0.get()
    E0x = asarray(E_field[0]).squeeze()
    E0y = asarray(E_field[1]).squeeze()

    angles = linspace(0, 360 * degrees, 90)
    Ex = real(E0x * exp(1j * angles))
    Ey = real(E0y * exp(1j * angles))

    max_size = (sqrt(Ex**2 + Ey**2)).max() * 1.1

    if limit in [0, '', [], None]:
        limit = max_size * 1.25

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(Ex, Ey, 'k', lw=2, label='polarized')
    if draw_arrow:
        ax.arrow(
            Ex[0],
            Ey[0],
            Ex[1] - Ex[0],
            Ey[1] - Ey[0],
            width=0,
            head_width=0.075 * max_size,
            fc='k',
            ec='k',
            length_includes_head=True)

    plt.axis('equal')
    plt.axis('square')
    plt.grid(True)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_xlabel('$E_x$', fontsize=22)
    ax.set_ylabel('$E_y$', fontsize=22)
    plt.tight_layout()

    if filename not in (None, [], ''):
        plt.savefig(filename)
    return fig, ax


def draw_ellipses_jones(Jones_vectors,
                        filename='',
                        has_legend=True,
                        draw_arrow=False):
    """Draws several one or several Jones vectors.

    Parameters:
        Jones_vectors (list or Jones_vector): Jones_vector or list of Jones vectors
        filename (str): name of filename to save the figure.
        has_legend (bool): prints legend
        draw_array (bool): draws chirality of ellipses
    """

    colors = [
        'k', 'r', 'g', 'b', 'k--', 'r--', 'g--', 'b--', 'k-.', 'r-.', 'g-.',
        'b-.'
    ]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    plt.axis('square')

    if Jones_vectors is not None:
        Jones_vectors = asarray(Jones_vectors)
        for i, ji in enumerate(Jones_vectors):
            E0x = asarray(ji.M[0]).squeeze()
            E0y = asarray(ji.M[1]).squeeze()
            angles = linspace(0, 360 * degrees, 90)

            Ex = real(E0x * exp(1j * angles))
            Ey = real(E0y * exp(1j * angles))

            max_size = (sqrt(Ex**2 + Ey**2)).max() * 1.1

            i_color = remainder(i, len(colors))
            ax.plot(Ex, Ey, colors[i_color], lw=2, label=ji.name)
            if draw_arrow:
                ax.arrow(
                    Ex[0],
                    Ey[0],
                    Ex[1] - Ex[0],
                    Ey[1] - Ey[0],
                    width=0,
                    head_width=0.075 * max_size,
                    fc=colors[i_color][0],
                    ec=colors[i_color][0],
                    length_includes_head=True)

    # ax.set_xticklabels([])
    # ax.set_yticklabels([])
    plt.grid(True)

    ax.set_xlabel('$E_x$', fontsize=22)
    ax.set_ylabel('$E_y$', fontsize=22)

    max_size = (sqrt(Ex**2 + Ey**2)).max() * 1.1
    ax.set_xlim(-max_size, max_size)
    ax.set_ylim(-max_size, max_size)
    if has_legend:
        plt.legend()
    plt.tight_layout()
    if filename not in (None, [], ''):
        plt.savefig(filename)

    return ax, fig


def draw_ellipse_stokes(stokes_0,
                        kind='',
                        limit='',
                        has_line=True,
                        filename=''):
    """ Draws polarization ellipse in stokes vector. If unpolarized light is present, a distribution of probability is given.

    Parameters:
        stokes_0 (Stokes): Stokes vector
        kind (str): 'line' 'probabilities'. 'Line': polarized + unpolarized ellipses. 'probabilities' is for unpolarized. Provides probabilities'
        limit (float): limit for drawing. If empty itis obtained from ampltiudes
        has_line (bool or float): If True  draws polarized and 0.1 probability lines. If it is a number draws that probability.
        filename (str): if filled, name for drawing

    Returns:
        ax (handle): handle to axis.
        fig (handle): handle to figure.
    """

    parameters = stokes_0.parameters.get_all()

    E0x, E0y, E0_unpol = parameters['amplitudes']
    delay = parameters['delay']

    angles = linspace(0, 360 * degrees, 256)
    Ex = E0x * cos(angles)
    Ey = E0y * cos(angles + delay)
    E_unpolarized_x = E0_unpol * cos(angles)
    E_unpolarized_y = E0_unpol * sin(angles)

    if limit in [0, '', [], None]:
        radius_max = sqrt(
            ((Ex + E_unpolarized_x)**2 + (Ey + E_unpolarized_y)**2).max())
        limit = radius_max * 1.25

    x = linspace(-limit, limit, 256)
    y = linspace(-limit, limit, 256)
    X, Y = meshgrid(x, y)

    if abs(E0_unpol) < eps or kind == 'line':
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(Ex, Ey, 'k', lw=2, label='polarized')
        ax.plot(
            E_unpolarized_x, E_unpolarized_y, 'r--', lw=2, label='unpolarized')
        plt.grid(True)
    else:
        sigma = E0_unpol

        u_random = exp(-(X**2 + Y**2) / (sigma**2))

        ellipse_2D = zeros_like(X, dtype=float)
        i_positions, _, _ = nearest2(x, Ex)
        j_positions, _, _ = nearest2(y, Ey)
        ellipse_2D[j_positions, i_positions] = 1

        prob = fftconvolve(ellipse_2D, u_random, mode='same')
        prob = prob / prob.max()

        fig, ax, IDimage = draw2D(prob, x, y)
        if isinstance(has_line, (int, float)):
            plt.contour(
                x, y, prob, (has_line, ), colors=('w'), linestyles=('dashed'))
        if has_line is True:
            plt.contour(
                x, y, prob, (0.1, ), colors=('w'), linestyles=('dashed'))
        if has_line is not False:
            plt.plot(Ex, Ey, 'k', lw=1)

        plt.grid(False)

    plt.axis('equal')
    plt.axis('square')
    ax.set_xlabel('$E_x$', fontsize=22)
    ax.set_ylabel('$E_y$', fontsize=22)
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    plt.legend()
    plt.tight_layout()
    if filename not in (None, [], ''):
        plt.savefig(filename)
    return ax, fig


def set_aspect_equal_3d(ax):
    """Fix equal aspect bug for 3D plots."""
    xlim = (-1, 1)
    ylim = (-1, 1)
    zlim = (-1, 1)

    xmean = mean(xlim)
    ymean = mean(ylim)
    zmean = mean(zlim)

    plot_radius = max([
        abs(lim - mean_)
        for lims, mean_ in ((xlim, xmean), (ylim, ymean), (zlim, zmean))
        for lim in lims
    ])

    factor = 1
    ax.set_xlim3d([xmean - factor * plot_radius, xmean + factor * plot_radius])
    ax.set_ylim3d([ymean - factor * plot_radius, ymean + factor * plot_radius])
    ax.set_zlim3d([zmean - 1 * plot_radius, zmean + 1 * plot_radius])
