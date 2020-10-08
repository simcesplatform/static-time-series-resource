# -*- coding: utf-8 -*-
'''
Contains classes related to reading the resource state from a csv file.
'''
from dataclasses import dataclass

import csv

@dataclass
class ResourceState():
    '''
    Represents resource state read from the csv file.
    ''' 
    
    bus: str
    real_power: float
    reactive_power: float
    node: int = None

class CsvFileError(Exception):
    '''
    CsvFileResourceStateSource was unable to read the given csv file or the file was missing a required column.
    '''    

class CsvFileResourceStateSource():
    '''
    Class for getting resource states from a csv file.
    '''
    
    def __init__(self, file_name: str, delimiter: str = ","  ):
        '''
        Create object which uses the given csv file that uses the given delimiter.
        Raises CsvFileError if file cannot be read e.g. file not found, or it is missing required columns.
        '''
        self._file = None # required if there is no file and the __del__ method is executed
        try:
            self._file = open( file_name, newline = "")
            
        except Exception as e:
            raise CsvFileError( f'Unable to read file {file_name}: {str( e )}.' )
        
        self._csv = csv.DictReader( self._file, delimiter = delimiter )
        # check that self._csv.fieldnames has required fields
        required_fields = set( [ 'RealPower', 'ReactivePower', 'Bus' ])
        fields = set( self._csv.fieldnames )
        # missing contains fields that do not exist or is empty if all fields exist.
        missing = required_fields.difference( fields )
        if len( missing ) > 0:
            raise CsvFileError( f'Resource state source csv file missing required columns: {",".join( missing )}.' )
        
    def __del__(self):
        '''
        Close the csv file when this object is destroyed.
        '''
        if self._file != None:
            self._file.close()
        
    def getNextEpochData(self) -> ResourceState:
        '''
        Get resource state for the next epoch i.e. read the next csv file row and return its contents.
        '''
        row = next( self._csv )
        real_power = float( row["RealPower"] )
        reactive_power = float( row["ReactivePower"] )
        bus = row["Bus"]
        node = row.get("Node")
        if node != None:
            if node == '':
                node = None
                
            else:
                node = int( node )
                 
        state = ResourceState( bus = bus, real_power = real_power, reactive_power = reactive_power, node = node)
        return state