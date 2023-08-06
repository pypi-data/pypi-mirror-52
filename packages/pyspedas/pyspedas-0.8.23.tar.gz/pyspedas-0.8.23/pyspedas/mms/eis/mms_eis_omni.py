


import numpy as np
from pytplot import get_data, store_data, options
from ...utilities.tnames import tnames

def mms_eis_omni(probe, species='proton', datatype='extof', suffix='', data_units='flux', data_rate='srvy'):

    probe = str(probe)
    species_str = datatype+'_'+species
    if data_rate == 'brst':
        prefix = 'mms'+probe+'_epd_eis_brst_'
    else: prefix = 'mms'+probe+'_epd_eis_'

    telescopes = tnames(pattern=prefix + species_str + '_*' + data_units + '_t?'+suffix)

    if len(telescopes) > 0:
        time, data, energies = get_data(telescopes[0])
        flux_omni = np.zeros((len(time), len(energies)))
        for t in telescopes:
            time, data, energies = get_data(t)
            flux_omni = flux_omni + data

        store_data(prefix+species_str+'_'+data_units+'_omni'+suffix, data={'x': time, 'y': flux_omni/6., 'v': energies})
        options(prefix+species_str+'_'+data_units+'_omni'+suffix, 'spec', 1)
        options(prefix+species_str+'_'+data_units+'_omni'+suffix, 'ylog', 1)
        options(prefix+species_str+'_'+data_units+'_omni'+suffix, 'zlog', 1)
        options(prefix+species_str+'_'+data_units+'_omni'+suffix, 'yrange', [14, 45])
        options(prefix+species_str+'_'+data_units+'_omni'+suffix, 'Colormap', 'jet')
        print(prefix+species_str+'_'+data_units+'_omni'+suffix)
