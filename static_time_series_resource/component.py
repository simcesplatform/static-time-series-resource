'''
Created on 23.9.2020

@author: hylli
'''
import asyncio

from tools.components import AbstractSimulationComponent
from tools.tools import FullLogger

LOGGER = FullLogger( __name__ )

class StaticTimeSeriesResource(AbstractSimulationComponent):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        
    async def start_epoch(self) -> bool:
        if not await super().start_epoch():
            return False
        
        LOGGER.info( 'Starting epoch.' )
        return True

async def start_component():
    resource = StaticTimeSeriesResource()
    await resource.start()
    while not resource.is_stopped:
        await asyncio.sleep( 2 )
        
if __name__ == '__main__':
    asyncio.run(start_component())