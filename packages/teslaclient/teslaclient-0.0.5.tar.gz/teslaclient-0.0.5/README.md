# Tesla API wrapper

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install TeslaClient
```bash
pip install TeslaClient
```

## Usage
```bash
Import TeslaClient

t = TeslaClient('email', 'password') # instantiates the client
t.connect() # connects to the api
v = t.vehicle('vehicle name') # creates an vehicle object based on case sensitive name
v.get_vehicle_data(*args) # accepts vehicle/climate/drive/charge_state or no parameter to collect all data. Loads data into a property dict of the same name
v.send_vehicle_command(command, data={}) # sends a command to vehicle, data parameter should contain any parameters required for command
```