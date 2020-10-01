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
    node: str = None
    

class CsvFileResourceStateSource():
    '''
    Class for getting resource states from a csv file.
    '''
    
    def __init__(self, file_name: str, delimiter: str = ","  ):
        '''
        Create object which uses the given csv file that uses the given delimiter.
        '''
        file = open( file_name, newline = "")
        self._csv = csv.DictReader( file, delimiter = delimiter )
        # check that self._csv.fieldnames has required fields
        
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
            node = int( node ) 
        state = ResourceState( bus = bus, real_power = real_power, reactive_power = reactive_power, node = node)
        return state