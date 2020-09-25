'''
Created on 23.9.2020

@author: hylli
'''
import asyncio

from tools.components import AbstractSimulationComponent
from tools.tools import FullLogger, load_environmental_variables
from tools.messages import ResourceStatesMessage

RESOURCE_STATES_TOPIC = "RESOURCE_STATES_TOPIC"
RESOURCE_TYPE = "RESOURCE_TYPE"

ACCEPTED_RESOURCE_TYPES = [ "Load", "Generator" ]

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
        environment = load_environmental_variables( 
            (RESOURCE_STATES_TOPIC, str, "ResourceStates"),
            ( RESOURCE_TYPE, str, None )
            )
        self._type = environment[ RESOURCE_TYPE ]
        if self._type == None or self._type not in ACCEPTED_RESOURCE_TYPES:
            # cannot continue do something 
            pass
        
        self._resource_states_topic = environment[ RESOURCE_STATES_TOPIC ]
        self._result_topic = '.'.join( [ self._resource_states_topic, self._type, self.component_name ])
        
    async def start_epoch(self) -> bool:
        if not await super().start_epoch():
            return False
        
        LOGGER.info( 'Starting epoch.' )
        await self._send_resource_states_message()
        
        return True
    
    async def _send_resource_states_message(self):
        resourceState = self._get_resource_states_message()
        await self._rabbitmq_client.send_message(self._result_topic, resourceState.bytes())
        
    def _get_resource_states_message(self) -> ResourceStatesMessage:
        message = ResourceStatesMessage(
            SimulationId = self.simulation_id,
            Type = ResourceStatesMessage.CLASS_MESSAGE_TYPE,
            SourceProcessId = self.component_name,
            MessageId = next(self._message_id_generator),
            EpochNumber = self._latest_epoch,
            TriggeringMessageIds = self._triggering_message_ids,
            Bus = "bus1",
            RealPower = 100.0,
            ReactivePower = 10.0
            )
        
        return message

async def start_component():
    resource = StaticTimeSeriesResource()
    await resource.start()
    while not resource.is_stopped:
        await asyncio.sleep( 2 )
        
if __name__ == '__main__':
    asyncio.run(start_component())