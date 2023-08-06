import json
import logging
import time
import sys
import requests

logging.basicConfig(filename='pyowlet.log', level=logging.DEBUG)


class PyOwlet(object):

    def __init__(self, username, password, prop_ttl=15):
        self.auth_token = None
        self.expire_time = 0
        self.prop_expire_time = 0
        self.prop_ttl = prop_ttl
        self.app_active_expire = 0
        self.app_active_ttl = 5
        self.username = username
        self.password = password
        self.headers = None
        self.auth_header = None
        self.monitored_properties = []
        self.app_active_prop_id = None

        self.auth_token = self.login(username, password)
        self.dsn = self.get_dsn()

        self.update_properties()

    def get_auth_header(self):
        '''
        Get the auth token. If the current token has not expired, return that.
        Otherwise login and get a new token and return that token.
        '''

        # if the auth token doesnt exist or has expired, login to get a new one
        if (self.auth_token is None) or (self.expire_time <= time.time()):
            logging.debug('Auth Token expired, need to get a new one')
            self.login(self.username, self.password)

        self.auth_header = {'content-type': 'application/json',
                            'accept': 'application/json',
                            'Authorization': 'auth_token ' + self.auth_token
                            }

        return self.auth_header

    def get_dsn(self):
        dsnurl = 'https://ads-field-1a2039d9.aylanetworks.com/apiv1/devices.json'
        response = requests.get(dsnurl, headers=self.get_auth_header())
        # data = auth_header(url)
        json_data = response.json()
        # FIXME: this is just returning the first device in the list
        # dsn = json_data[0]['device']['dsn']
        return json_data[0]['device']['dsn']

    def get_properties(self, measure=None, set_active=True):

        if set_active is True:
            self.set_app_active()

        properties_url = 'https://ads-field-1a2039d9.aylanetworks.com/apiv1/dsns/{}/properties'.format(
            self.dsn)

        if measure is not None:
            properties_url = properties_url + '/' + measure

        response = requests.get(properties_url, headers=self.get_auth_header())
        data = response.json()

        if measure is not None:
            return data['property']

        return data

    def set_app_active(self):

        if self.app_active_expire < time.time():

            if self.app_active_prop_id is None:
                prop = self.get_properties('APP_ACTIVE', False)
                self.app_active_prop_id = prop['key']

            data_point_url = 'https://ads-field-1a2039d9.aylanetworks.com/apiv1/properties/{}/datapoints.json'.format(
                self.app_active_prop_id)

            payload = {'datapoint': {'value': 1}}
            resp = requests.post(
                data_point_url,
                json=payload,
                headers=self.get_auth_header()
            )

            self.app_active_expire = time.time() + self.app_active_ttl

    def update_properties(self):

        self.set_app_active()

        data = self.get_properties()

        for value in data:
            name = value['property']['name'].lower()
            val = value['property']['value']

            if name not in self.monitored_properties:
                self.monitored_properties.append(name)

            self.__setattr__(name, val)

        self.prop_expire_time = time.time() + self.prop_ttl

    def __getattribute__(self, attr):

        monitored = object.__getattribute__(self, 'monitored_properties')
        prop_exp = object.__getattribute__(self, 'prop_expire_time')

        if attr in monitored and prop_exp <= time.time():
            self.update_properties()

        return object.__getattribute__(self, attr)

    def login(self, email, password):
        """Logs in to the Owlet API service to get access token.

        Returns:
        A json value with access token.
        """
        self.headers = {'content-type': 'application/json',
                        'accept': 'application/json'}
        login_url = 'https://user-field-1a2039d9.aylanetworks.com/users/sign_in.json'
        login_payload = {
            "user": {
                "email": email,
                "password": password,
                "application": {
                    "app_id": "OWL-id",
                    "app_secret": "OWL-4163742"
                }
            }
        }
        logging.debug('Generating token')
        data = requests.post(
            login_url,
            json=login_payload,
            headers=self.headers
        )
        # Example response:
        # {
        #    u'access_token': u'abcdefghijklmnopqrstuvwxyz123456',
        #    u'role': u'EndUser',
        #    u'expires_in': 86400,
        #    u'refresh_token': u'123456abcdefghijklmnopqrstuvwxyz',
        #    u'role_tags': []
        # }

        json_data = data.json()
        # update our auth token
        self.auth_token = json_data['access_token']

        # update our auth expiration time
        self.expire_time = time.time() + json_data['expires_in']

        logging.debug('Auth Token: %s expires at %s',
                      self.auth_token, self.expire_time)
        # return auth_token
        # return expire_time
