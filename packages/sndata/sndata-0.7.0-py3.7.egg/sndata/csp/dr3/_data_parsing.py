#!/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

"""This module defines functions for accessing locally available data files."""

import numpy as np
from astropy.io import ascii

from . import _meta as meta
from ... import _integrations as integrations
from ... import _utils as utils


@utils.require_data_path(meta.data_dir)
def register_filters(force=False):
    """Register filters for this survey / data release with SNCosmo

    Args:
        force (bool): Whether to re-register a band if already registered
    """

    for _file_name, _band_name in zip(meta.filter_file_names, meta.band_names):
        filter_path = meta.filter_dir / _file_name
        integrations.register_filter(filter_path, _band_name, force=force)


@utils.require_data_path(meta.data_dir)
def get_available_tables():
    """Get table numbers for machine readable tables published in the paper
    for this data release"""

    file_list = meta.table_dir.glob('*.dat')
    return [int(table_path.stem.strip('table')) for table_path in file_list]


@utils.require_data_path(meta.data_dir)
def load_table(table_id):
    """Load a table from the data paper for this survey / data

    See ``get_available_tables`` for a list of valid table IDs.

    Args:
        table_id (int, str): The published table number or table name
    """

    readme_path = meta.table_dir / 'ReadMe_formatted'
    table_path = meta.table_dir / f'table{table_id}.dat'
    if table_id not in get_available_tables():
        raise ValueError(f'Table {table_id} is not available.')

    data = ascii.read(str(table_path), format='cds', readme=str(readme_path))
    description = utils.read_vizier_table_descriptions(readme_path)[table_id]
    data.meta['description'] = description
    return data


@utils.require_data_path(meta.data_dir)
def get_available_ids():
    """Return a list of target object IDs for the current survey

    Returns:
        A list of object IDs as strings
    """

    files = meta.photometry_dir.glob('*.txt')
    return sorted(f.stem.split('_')[0].lstrip('SN') for f in files)


def _get_zp_for_bands(band):
    """Returns the zero point corresponding to any band in meta.band_names

    Args:
        band (list[str]): The name of a band

    Returns:
        An array of zero points
    """

    sorter = np.argsort(meta.band_names)
    indices = np.searchsorted(meta.band_names, band, sorter=sorter)

    return np.array(meta.zero_point)[sorter[indices]]


@utils.require_data_path(meta.data_dir)
def get_data_for_id(obj_id, format_table=True):
    """Returns data for a given object ID

    See ``get_available_ids()`` for a list of available ID values.

    Args:
        obj_id        (str): The ID of the desired object
        format_table (bool): Format data for ``SNCosmo`` (Default: True)

    Returns:
        An astropy table of data for the given ID
    """

    # Read data file for target
    file_path = meta.photometry_dir / f'SN{obj_id}_snpy.txt'
    data_table = integrations.parse_snoopy_data(file_path)
    data_table.meta['obj_id'] = data_table.meta['obj_id'].lstrip('SN')

    if format_table:
        # Convert band names to package standard
        data_table['band'] = 'csp_dr3_' + data_table['band']

        offsets = np.array([meta.instrument_offsets[b] for b in data_table['band']])
        data_table['mag'] += offsets

        # Add flux values
        data_table['zp'] = _get_zp_for_bands(data_table['band'])
        data_table['zpsys'] = np.full(len(data_table), 'ab')
        data_table['flux'] = 10 ** ((data_table['mag'] - data_table['zp']) / -2.5)
        data_table['fluxerr'] = np.log(10) * data_table['flux'] * data_table['mag_err'] / 2.5

    return data_table


iter_data = utils.factory_iter_data(get_available_ids, get_data_for_id)
