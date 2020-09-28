'''
Created on 25.9.2020

@author: hylli
'''
from dataclasses import dataclass

import csv

@dataclass
class ResourceState():
    
    bus: str
    real_power: float
    reactive_power: float
    node: str = None
    

class CsvFileResourceStateSource():
    
    def __init__(self, file_name: str, delimiter: str = ","  ):
        file = open( file_name, newline = "")
        self._csv = csv.DictReader( file, delimiter = delimiter )
        # check that self._csv.fieldnames has required fields
        
    def getNextEpochData(self) -> ResourceState:
        row = next( self._csv )
        real_power = float( row["RealPower"] )
        reactive_power = float( row["ReactivePower"] )
        bus = row["Bus"]
        node = row.get("Node")
        if node != None:
            node = int( node ) 
        state = ResourceState( bus = bus, real_power = real_power, reactive_power = reactive_power, node = node)
        return state