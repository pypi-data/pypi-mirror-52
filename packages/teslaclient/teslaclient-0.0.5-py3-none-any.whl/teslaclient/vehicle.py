import requests
import pprint


BASE_URL = 'https://owner-api.teslamotors.com'
API_BASE = BASE_URL + '/api/1'


class Vehicle:

    def __init__(self, id, header):
        self._id = id
        self.header = header
        self._drive_state = None
        self._climate_state = None
        self._charge_state = None
        self._vehicle_state = None
        self._vehicle_api_base = f'{API_BASE}/vehicles/{self._id}'
        self._connection_status = None
        self.get_vehicle_data()
        

    @property
    def connection_status(self):
        return self._connection_status
        
    @property
    def id(self):
        return self._id
    
    @property
    def drive_state(self):
        return self._drive_state

    @property
    def climate_state(self):
        return self._climate_state

    @property
    def charge_state(self):
        return self._charge_state
    
    @property
    def vehicle_state(self):
        return self._vehicle_state
    

    def get_vehicle_data(self, *args):
        '''
            gets complete vehicle state of vehicle
        '''
        if len(args) == 0:
            r = requests.get(f'{self._vehicle_api_base}/vehicle_data', headers=self.header)
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                self._connection_status = e.response.status_code
            
            if r.status_code ==200:
                self._drive_state = r.json()['response']['drive_state']
                self._climate_state = r.json()['response']['climate_state']
                self._charge_state = r.json()['response']['charge_state']
                self._vehicle_state = r.json()['response']['vehicle_state']

        else:
            for a in args:
                r = requests.get(f'{self._vehicle_api_base}/data_request/{a}', headers=self.header)
                try:
                    r.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    pprint.pprint(e)

                if r.status_code ==200:
                    if a == 'drive_state':
                        self._drive_state = r.json()['response']
                    elif a == 'climate_state':
                        self._climate_state = r.json()['response']
                    elif a == 'charge_state':
                        self._charge_state = r.json()['response']
                    elif a == 'vehicle_state':
                        self._vehicle_state = r.json()['response']
                    else:
                        raise NameError('Invalid data request')
        self._connection_status = r.status_code

    def send_vehicle_command(self, command, data={}):
        '''
            function that executes a command on the vehicle
        '''
        if command == 'wake_up':
            url = f'{self._vehicle_api_base}/wake_up'
        else:
            url = f'{self._vehicle_api_base}/command/{command}'

        r = requests.post(url, headers=self.header, data=data)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            pprint.pprint(e)
        
        if r.status_code == 200:
            self.get_vehicle_data()
            print(r.json())