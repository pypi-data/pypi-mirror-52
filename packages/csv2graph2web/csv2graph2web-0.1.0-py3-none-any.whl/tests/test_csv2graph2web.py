# -*- coding: utf-8 -*-

import unittest

import os
import stat
import shutil
import glob


from csv2graph2web import csv2graph2web as cgw
from csv2graph2web import cgw_copy

csv_filename = '__cgw__.csv'

class tests( unittest.TestCase ):
###################################################################
    @classmethod
    def setUpClass(cls): # it is called before tests starting
        with open( csv_filename, 'w' ) as fout:
            line = 'iter, x, y'
            fout.write( line+'\n' )
            for i in range(10):
                line = '{}, {}, {}'.format( i, 2*i, i*i )
                fout.write( line+'\n' )

        if( os.path.exists( 'cgw.cgi' ) ):
            os.remove( 'cgw.cgi' )
        if( os.path.exists( 'graphs' ) ):
            shutil.rmtree( 'graphs' )
        if( os.path.exists( 'tmp' ) ):
            shutil.rmtree( 'tmp' )
        pass

    @classmethod
    def tearDownClass(cls): # it is called before tests ending
        os.remove( csv_filename )
        if( os.path.exists( 'cgw.cgi' ) ):
            os.remove( 'cgw.cgi' )
        if( os.path.exists( 'graphs' ) ):
            shutil.rmtree( 'graphs' )
        if( os.path.exists( 'tmp' ) ):
            shutil.rmtree( 'tmp' )
        pass

    def setUp(self): # it is called before each test
        pass

    def tearDown(self): # it is called after each test
        pass

###################################################################
    def test_copy(self):
        cgw_copy.main()

        s = stat.S_IMODE(os.stat('cgw.cgi').st_mode)
        self.assertTrue( s == 0o555 )

        s = stat.S_IMODE(os.stat('graphs').st_mode)
        self.assertTrue( s == 0o777 )

    def test_graph(self):
        graph_params = []
        opt = {'xlabel':'Iter', 'legend':True}

        opt['title'] = 'x'
        graph_params.append( ([('iter', 'x')], opt.copy()) )
        opt['title'] = 'y'
        graph_params.append( ([(0, 2)], opt.copy()) )
        opt['title'] = 'xy'
        graph_params.append( ([(0, 1), ('iter','y')], opt.copy()) )

        cgw.csv2graph2web( URL=None, dir_name='tmp', csv_filename=csv_filename, graph_params=graph_params )

        files = glob.glob( 'tmp/*.png' )

        self.assertTrue( 'tmp/000.png' in files )
        self.assertTrue( 'tmp/001.png' in files )
        self.assertTrue( 'tmp/002.png' in files )


###################################################################
    def suite():
        suite = unittest.TestSuite()
        suite.addTests(unittest.makeSuite(tests))
        return suite

