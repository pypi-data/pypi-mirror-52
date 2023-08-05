#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2017-2019 Airinnova AB and the PyTornado authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Authors:
# * Alessandro Gastaldi
# * Aaron Dettmann

"""
Functions for writing of PyTornado VLM results.

Developed at Airinnova AB, Stockholm, Sweden.
"""

import os
import logging

import numpy as np
from commonlibs.logger import truncate_filepath

from pytornado.objects.vlm_struct import VLMLattice
import pytornado.aero.vlm as vlm
from pytornado.fileio.utils import dump_pretty_json

logger = logging.getLogger(__name__)


def save_all(settings, aircraft, state, vlmdata, lattice):
    """
    Evaluate all 'save' settings and create result files

    Args:
        :settings: settings instance
        :aircraft: (object) data structure for aircraft model
        :state: (object) data structure for operating conditions
        :vlmdata: (object) data structure for VLM calculation data
        :lattice: (object) data structure for VLM lattice
    """

    if settings.settings['save_results']['global']:
        _save_glob_results(state, vlmdata, settings)

    if settings.settings['save_results']['panelwise']:
        _save_panelwise(state, vlmdata, settings)


def _save_glob_results(state, vlmdata, settings):
    """
    Save global results

    Args:
        :state: (object) data structure for operating conditions
        :vlmdata: (object) data structure for VLM calculation data
        :settings: (object) data structure for execution settings
    """

    filepath = settings.paths('f_results_global')
    logger.info(f"Writing global results to file '{truncate_filepath(filepath)}'")

    output = {}
    output['aero'] = {k: v for k, v in state.aero.items()}
    output['refs'] = {k: v for k, v in state.refs.items()}
    output['global_forces'] = {k: v for k, v in vlmdata.forces.items()}
    output['global_coeffs'] = {k: v for k, v in vlmdata.coeffs.items()}

    with open(filepath, "w") as fp:
        dump_pretty_json(output, fp)


def _save_panelwise(state, vlmdata, settings):
    """
    Save panelwise results

    Args:
        :state: (object) data structure for operating conditions
        :vlmdata: (object) data structure for VLM calculation data
        :settings: (object) data structure for execution settings
    """

    filepath = settings.paths('f_results_panelwise')
    logger.info(f"Writing panelwise results to file '{truncate_filepath(filepath)}'")

    data_keys = [
        ('gamma', 'm^2/s'),
        ('vx', 'm/s'),
        ('vy', 'm/s'),
        ('vz', 'm/s'),
        ('vmag', 'm/s'),
        ('fx', 'N'),
        ('fy', 'N'),
        ('fz', 'N'),
        ('fmag', 'N'),
        ('cp', '1'),
    ]

    # ----- Data and formatting -----
    data = np.stack([vlmdata.panelwise[data_key] for (data_key, _) in data_keys], axis=-1)
    fmt = ['%13.6e' for _ in data_keys]

    # ----- Header -----
    field_size = 12
    header = ''
    for i, (data_key, unit) in enumerate(data_keys):
        header += f'{data_key} [{unit}]'.center(field_size)
        field_size = 14

    # ----- Save -----
    np.savetxt(
        filepath,
        data,
        delimiter=',',
        header=header,
        fmt=fmt,
        comments='# '
    )


# ===========================================================================
# ===========================================================================
# ===========================================================================
# def _save_loads(aircraft, settings, state, vlmdata, lattice=None):
#     """
#     Save computed loads in a JSON file

#     Note:
#         * If lattice is None, the lattice in the undeformed state will be computed

#     Args:
#         :aircraft: (object) data structure for aircraft model
#         :settings: (object) data structure for execution settings
#         :vlmdata: (object) data structure for VLM calculation data
#         :lattice: (object) data structure for VLM lattice
#     """

#     # TODO:
#     # * Make better
#     # * Better way to deal with filenames

#     # Regenerate lattice for collocation points in undeformed state
#     if lattice is None:
#         logger.info("Regenerating lattice data of the undeformed state...")
#         aircraft.turn_off_all_deformation()
#         lattice = VLMLattice()
#         lattice = vlm.gen_lattice(aircraft, state, settings, make_new_subareas=False)
#         aircraft.turn_on_all_deformation()

#     for wing_uid, panellist in lattice.bookkeeping_by_wing_uid.items():
#         output = []
#         for entry in panellist:
#             for i in entry.pan_idx:
#                 force_point = lattice.bound_leg_midpoints[i]

#                 fx = vlmdata.panelwise['fx'][i]
#                 fy = vlmdata.panelwise['fy'][i]
#                 fz = vlmdata.panelwise['fz'][i]
#                 output.append({"coord": list(force_point), "load": [fx, fy, fz, 0, 0, 0]})

#         filepath = os.path.join(settings.paths('d_results'), f"loads_UID_{wing_uid}.json")
#         logger.info(f"Writing loads to file '{truncate_filepath(filepath)}'")
#         with open(filepath, "w") as fp:
#             dump_pretty_json(output, fp)

#     for wing_uid, panellist in lattice.bookkeeping_by_wing_uid_mirror.items():
#         output = []
#         for entry in panellist:
#             for i in entry.pan_idx:
#                 force_point = lattice.bound_leg_midpoints[i]

#                 fx = vlmdata.panelwise['fx'][i]
#                 fy = vlmdata.panelwise['fy'][i]
#                 fz = vlmdata.panelwise['fz'][i]
#                 output.append({"coord": list(force_point), "load": [fx, fy, fz, 0, 0, 0]})

#         filepath = os.path.join(settings.paths('d_results'), f"loads_mirror_UID_{wing_uid}.json")
#         logger.info(f"Writing loads to file '{truncate_filepath(filepath)}'")
#         with open(filepath, "w") as fp:
#             dump_pretty_json(output, fp)
# ===========================================================================
# ===========================================================================
# ===========================================================================


def save_aeroperformance_map(state, settings):
    """
    Save the aeroperformance map

    Args:
        :state: (object) data structure for operating conditions
        :settings: (object) data structure for execution settings
    """

    filepath = settings.paths('f_results_apm_global')
    logger.info(f"Writing aeroperformance map results to '{truncate_filepath(filepath)}'")

    output = {}
    for dictionary in [state.aero, state.results]:
        for k, v in dictionary.items():
            output[k] = list(v) if v is not None else []

    with open(filepath, "w") as fp:
        dump_pretty_json(output, fp)
