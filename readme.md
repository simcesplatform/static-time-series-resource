# Static time series resource

A simulation platform component used to simulate simple loads and generators whose published states are determined by a file containing a simple time series of attribute values for each epoch.

## Requirements

- python 3.7
- pip for installing requirements

Install requirements:

```bash
# optional create a virtual environment:
python3 -m venv .env
# activate it
. .env/bin/activate # *nix
.env\scripts\activate # windows.
# install required packages
pip install -r requirements.txt
```

## Usage

The component is based on the AbstractSimulationCompoment class from the [simulation-tools](..//simulation-tools)
 repository. It is configured via environment variables which include common variables for all AbstractSimulationComponent subclasses such as rabbitmq connection and component name. Environment variables specific to this component are listed below:
 
- RESOURCE_STATE_TOPIC (optional): The upper level topic under whose subtopics the resource states are published. If this environment variable is not present ResourceState is used.
- RESOURCE_TYPE (required): Type of this resource. Accepted values are Generator or Load.
- RESOURCE_STATE_CSV_FILE (required): Location of the csv file which contains the resource state information used in the simulation. Relative file paths are in relation to the current working directory.
- RESOURCE_STATE_CSV_DELIMITER (optional): Delimiter used in the csv file. The default is ,

The csv file should contain columns named after the ResourceState message attributes: RealPower, ReactivePower, Bus and Node. The Node column is optional. Each row containing values will then represent data for one epoch. There should be at least as many data rows as there will be epochs. 

The component can be launched with:

    python -m static_time_series_resource.component

Docker can be used with the included docker file

## Demo

The [demo](demo) directory includes everything required for running a docker compose based demo with this component which uses  all other base simulation platform components: simulation manager, log writer and log reader. It is based on a [similar demo](../simulation-manager/-/tree/master/docker-files) 
for the simulation manager which uses dummy componets. This demo assumes that all required simulation platform repositories including this one are cloned under the same parent directory. A test simulation can then be launched from the demo directory by running:

    ./start_simulation.sh

Simulation parameters can be changed by modifying the env files in the env directory. The simulation includes two resources called load1 and generator1. The resource state data they use are in the load1.csv and generator1.csv files. The simulation includes 5 epochs.     