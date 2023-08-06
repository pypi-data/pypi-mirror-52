# -*- coding: utf-8 -*-

import os
try:
    # python 2
    from StringIO import StringIO as io_memory
except ImportError:
    # python 3
    from io import BytesIO as io_memory

import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def csv2graph2web( URL, dir_name, csv_filename, graph_params ):
    df = pd.read_csv( csv_filename, skipinitialspace=True )

    if( URL is None ):
        os.makedirs( dir_name, exist_ok=True )
        for i, param in enumerate( graph_params ):
            filename = os.path.join( dir_name, f'{i:03d}.png' )
            save_graph( df, param[0], param[1], filename )

    else:
        for i, param in enumerate(graph_params):
            buffer = io_memory()
            save_graph( df, param[0], param[1], buffer )
            buffer.seek(0)
            file = { 'file': buffer }
            data = { 'dirname': dir_name, 'filename': f'{i:03d}.png' }
            res = requests.post(URL, data=data, files=file)


def save_graph( df, axes, opt, filename ):
    plt.clf()
    for axis in axes:
        x = []
        for i in range(2):
            if( isinstance( axis[i], int ) ):
                x.append( df[df.columns[axis[i]]] )
                label = df.columns[axis[i]]
            elif( isinstance( axis[i], str ) ):
                x.append( df[axis[i]] )
                label = axis[i]
            else:
                raise NotImplementedError
        plt.plot( x[0], x[1], label=label )

    opt = CaseInsensitiveDict( opt )
    if( 'title' in opt ): plt.title( opt['title'] )
    if( 'xlabel' in opt ): plt.xlabel( opt['xlabel'] )
    if( 'ylabel' in opt ): plt.ylabel( opt['ylabel'] )
    if( 'legend' in opt and opt['legend'] == True ): plt.legend(loc='best')

    plt.savefig(filename)

