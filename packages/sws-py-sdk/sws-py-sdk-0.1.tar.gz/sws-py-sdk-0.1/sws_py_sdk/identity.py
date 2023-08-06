""" This file exposes endpoints from the SWS Identity Service
"""

from requests.auth import HTTPBasicAuth

from sws_py_sdk.service import Service

class Identity(Service):

    def __init__(self, sws):
        super().__init__(sws)
        self.service_uri = sws.service_uris['id']

    def token_refresh(self, refresh_token):
        """ Endpoint for refreshing access tokens
            refresh_token : string
                Refresh token for user that proves they deserve a new access token.
        """
        return self.fetch(
            auth=None,
            endpoint='/api/v1/me/tokens/refresh',
            body={'refresh_token': refresh_token},
            method='POST'
        )

    def login(self, email_address, password, device_id, device_name):
        """ Logs user in with Basic auth
            email_address : string
                User's email address
            password : str
                User's password
            device_id : str
                Some identifier of the machine
            device_name : str
                Human readable name of machine
        """
        return self.fetch(
            auth=HTTPBasicAuth(self.sws.app_id, self.sws.app_secret),
            endpoint='/api/v1/login',
            body={
                'email_address': email_address,
                'password': password,
                'device_id': device_id,
                'device_name': device_name
            },
            method='POST'
        )
