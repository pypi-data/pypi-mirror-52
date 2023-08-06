import requests
import pprint
import json
from vehicle import Vehicle

BASE_URL = 'https://owner-api.teslamotors.com'
API_BASE = BASE_URL + '/api/1'
OAUTH_URL = BASE_URL + '/oauth/token'


client_id = '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
client_secret = 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'

class TeslaClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self._access_token = None
        self._refresh_token = None
        self._oauth_body = None
        self._header = {'User-Agent': 'application/json'}
        self._connection_status = None
    
    @property
    def connection_status(self):
        return self._connection_status
    
    @property
    def header(self):
        return self._header

    def connect(self):
        if self._access_token is None:
            self._oauth_body = {
                'grant_type':'password',
                'client_id':client_id,
                'client_secret':client_secret,
                'email':self.email,
                'password':self.password
            }
        else:
            self._oauth_body = {
                'grant_type':'refresh_token',
                'client_id':client_id,
                'client_secret':client_secret,
                'refresh_token':self._refresh_token
            }
        r = requests.post(OAUTH_URL, headers=self._header, data=self._oauth_body)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            pprint.pprint(e)

        if r.status_code == 200:
            self._access_token = r.json()['access_token']
            self._refresh_token = r.json()['refresh_token']
            self._header['Authorization'] = f'Bearer {self._access_token}'
            self._connection_status = r.status_code

        
        
    def list_vehicles(self):
        if self._access_token is None:
            self.connect()
        
        r = requests.get(f'{API_BASE}/vehicles', headers=self.header)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            pprint.pprint(e)
        
        if r.status_code == 200:
            return r.json()['response']
        
        
    def vehicle(self, name):
        vehicle_list = self.list_vehicles()
        for v in vehicle_list:
            if v['display_name'] == name:
                return Vehicle(v['id'], self.header)
            else:
                pprint.pprint(f'{name} not found')
    