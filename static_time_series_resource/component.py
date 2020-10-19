# -*- coding: utf-8 -*-
'''
Contains class for a simulation platform component used to simulate simple loads and generators whose published states are determined by a file containing a simple time series of attribute values for each epoch.
'''
import asyncio

from tools.components import AbstractSimulationComponent
from tools.tools import FullLogger, load_environmental_variables
from tools.messages import ResourceStateMessage

from static_time_series_resource.data_source import CsvFileResourceStateSource 

# names of used environment variables
RESOURCE_STATE_TOPIC = "RESOURCE_STATE_TOPIC"
RESOURCE_TYPE = "RESOURCE_TYPE"
RESOURCE_STATE_CSV_FILE = "RESOURCE_STATE_CSV_FILE"
RESOURCE_STATE_CSV_DELIMITER = "RESOURCE_STATE_CSV_DELIMITER"  

# allowed values for resource type
ACCEPTED_RESOURCE_TYPES = [ "Load", "Generator" ]

LOGGER = FullLogger( __name__ )

class StaticTimeSeriesResource(AbstractSimulationComponent):
    '''
    A simulation platform component used to simulate simple loads and generators whose published states are determined by a file containing a simple time series of attribute values for each epoch.
    '''

    def __init__(self, stateSource: CsvFileResourceStateSource):
        '''
        Create a component which uses the given csv state source for its published resource states.
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
        # publish resource states to this topic
        self._result_topic = '.'.join( [ self._resource_state_topic, self._type, self.component_name ])
        
    async def start_epoch(self) -> bool:
        '''
        Handle the start of an epoch by publishing the resource state for the epoch.
        '''
        if not await super().start_epoch():
            return False
        
        LOGGER.debug( 'Starting epoch.' )
        try:
            await self._send_resource_state_message()
            
        except Exception as error:
            description = f'Unable to create or send a ResourceState message: {str( error )}'
            LOGGER.error( description )
            await self.send_error_message(description)
            return False
        
        return True
    
    async def _send_resource_state_message(self):
        '''
        Sends a ResourceState message for the current epoch.
        '''
        resourceState = self._get_resource_state_message()
        await self._rabbitmq_client.send_message(self._result_topic, resourceState.bytes())
        
    def _get_resource_state_message(self) -> ResourceStateMessage:
        '''
        Create a ResourceStateMessage from the next resource state info available from the state source.
        '''
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

def create_component() -> StaticTimeSeriesResource:
    '''
    Create a StaticTimeSeries resource initialized with a csv file resource state source.
    '''
    # get information about the used source csv file and create a state source that uses it
    environment = load_environmental_variables(
        ( RESOURCE_STATE_CSV_FILE, str ),
        ( RESOURCE_STATE_CSV_DELIMITER, str, "," )
        )
    
    stateSource = CsvFileResourceStateSource( environment[RESOURCE_STATE_CSV_FILE], environment[RESOURCE_STATE_CSV_DELIMITER]) 
    return StaticTimeSeriesResource(stateSource)

async def start_component():
    '''
    Start a StaticTimeSeriesResource component.
    '''
    resource = create_component() 
    await resource.start()
    while not resource.is_stopped:
        await asyncio.sleep( 2 )
        
if __name__ == '__main__':
    asyncio.run(start_component())