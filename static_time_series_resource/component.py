'''
Created on 23.9.2020

@author: hylli
'''
import asyncio

from tools.components import AbstractSimulationComponent
from tools.tools import FullLogger, load_environmental_variables
from tools.messages import ResourceStateMessage

from static_time_series_resource.data_source import CsvFileResourceStateSource 

RESOURCE_STATE_TOPIC = "RESOURCE_STATE_TOPIC"
RESOURCE_TYPE = "RESOURCE_TYPE"

RESOURCE_STATE_CSV_FILE = "RESOURCE_STATE_CSV_FILE"
RESOURCE_STATE_CSV_DELIMITER = "RESOURCE_STATE_CSV_DELIMITER"  

ACCEPTED_RESOURCE_TYPES = [ "Load", "Generator" ]

LOGGER = FullLogger( __name__ )

class StaticTimeSeriesResource(AbstractSimulationComponent):
    '''
    classdocs
    '''

    def __init__(self, stateSource: CsvFileResourceStateSource):
        '''
        Constructor
        '''
        super().__init__()
        self._stateSource = stateSource
        environment = load_environmental_variables( 
            (RESOURCE_STATE_TOPIC, str, "ResourceState"),
            ( RESOURCE_TYPE, str, None )
            )
        self._type = environment[ RESOURCE_TYPE ]
        if self._type == None or self._type not in ACCEPTED_RESOURCE_TYPES:
            # cannot continue do something 
            pass
        
        self._resource_state_topic = environment[ RESOURCE_STATE_TOPIC ]
        self._result_topic = '.'.join( [ self._resource_state_topic, self._type, self.component_name ])
        
    async def start_epoch(self) -> bool:
        if not await super().start_epoch():
            return False
        
        LOGGER.info( 'Starting epoch.' )
        await self._send_resource_state_message()
        
        return True
    
    async def _send_resource_state_message(self):
        resourceState = self._get_resource_state_message()
        await self._rabbitmq_client.send_message(self._result_topic, resourceState.bytes())
        
    def _get_resource_state_message(self) -> ResourceStateMessage:
        state = self._stateSource.getNextEpochData()
        message = ResourceStateMessage(
            SimulationId = self.simulation_id,
            Type = ResourceStateMessage.CLASS_MESSAGE_TYPE,
            SourceProcessId = self.component_name,
            MessageId = next(self._message_id_generator),
            EpochNumber = self._latest_epoch,
            TriggeringMessageIds = self._triggering_message_ids,
            Bus = state.bus,
            RealPower = state.real_power,
            ReactivePower = state.reactive_power,
            Node = state.node
            )
        
        return message

async def start_component():
    environment = load_environmental_variables(
        ( RESOURCE_STATE_CSV_FILE, str ),
        ( RESOURCE_STATE_CSV_DELIMITER, str, "," )
        )
    
    stateSource = CsvFileResourceStateSource( environment[RESOURCE_STATE_CSV_FILE], environment[RESOURCE_STATE_CSV_DELIMITER]) 
    resource = StaticTimeSeriesResource(stateSource)
    await resource.start()
    while not resource.is_stopped:
        await asyncio.sleep( 2 )
        
if __name__ == '__main__':
    asyncio.run(start_component())