# -*- coding: utf-8 -*-
'''
Tests for the state_source module.
'''
import unittest
import pathlib

from static_time_series_resource.data_source import ResourceState, CsvFileResourceStateSource 

def getFilePath( fileName: str ) -> pathlib.Path:
    '''
    Get full path to test data files located in  the same directory as this file.
    '''
    return  pathlib.Path(__file__).parent.absolute() / fileName

class TestDataSource(unittest.TestCase):
    '''
    Tests for the csv resource state source.
    '''

    def testReadData(self):
        '''
        Test that csv is read correctly and converted correctly to ResourceState objects.
        '''
        # test with different files: define file name and ResourceStates expected to be created from it 
        scenarios = [
            { 'file': 'load1.csv',
              'expected': [
                  ResourceState( real_power = -10, reactive_power = -1, bus = 'bus1', node = None ),
                  ResourceState( real_power = -11.5, reactive_power = -2.0, bus = 'bus1', node = 1 ),
                  ResourceState( real_power = -9.1, reactive_power = 0, bus = 'bus1', node = 2 )
                  ] },
            # contains an Epoch field which is not used but should be allowed for human convenience
            { 'file': 'generator1.csv',
              'expected': [
                  ResourceState( real_power = 4.5, reactive_power = 0.5, bus = 'bus1' ),
                  ResourceState( real_power = 7.5, reactive_power = 1.0, bus = 'bus1' )
                  ] }
            ]
        
        for scenario in scenarios:
            fileName = scenario['file']
            expected = scenario['expected']
            with self.subTest( file = fileName ):
                stateSource = CsvFileResourceStateSource( getFilePath( fileName ))
                result = []
                for _ in range( 0, len( expected )):
                    result.append( stateSource.getNextEpochData())
                    
                self.assertEqual( result, expected )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDataSource']
    unittest.main()