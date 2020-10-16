# -*- coding: utf-8 -*-
'''
Tests for the state_source module.
'''
import unittest
import pathlib

from static_time_series_resource.data_source import ResourceState, CsvFileResourceStateSource, CsvFileError 

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
                
    def testMissingColumns(self):
        '''
        Check that missing RealPower, ReactivePower or Bus columns causes an exception.
        '''
        # each file has a different missing column
        files = [ 'invalid_fields1.csv', 'invalid_fields2.csv', 'invalid_fields3.csv' ]
        for file in files:
            with self.subTest( file = file ):
                with self.assertRaises( CsvFileError ) as cm:
                    CsvFileResourceStateSource( getFilePath(file) )
                
                # check that exception message is the correct one.
                self.assertTrue( str( cm.exception ).startswith( 'Resource state source csv file missing required columns:'), f'Exception message was {str( cm.exception )}.' )
                
    def testUnableToreadFile(self):
        '''
        Test that file not found raises the correct exception.
        '''
        with self.assertRaises( CsvFileError ) as cm:
            CsvFileResourceStateSource( 'foo.csv' )
            
        message = str( cm.exception )
        self.assertTrue( message.startswith( 'Unable to read file' ), f'Exception message was {message}.' )
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDataSource']
    unittest.main()