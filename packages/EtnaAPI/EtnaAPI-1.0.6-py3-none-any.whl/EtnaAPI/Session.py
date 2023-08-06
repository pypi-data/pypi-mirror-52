#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests as rq
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .Errors import *


class BasicController:
    module_api = "https://modules-api.etna-alternance.net"

    def __init__(self, session: 'Session'):
        self.session = session

    @property
    def req_session(self):
        return self.session.session


class Session:
    """
    Class managing a session
    """

    auth_url = "https://auth.etna-alternance.net"

    def __init__(self, request_retries=1, retry_on_statuses=(500, 502, 504)):
        self._is_authenticated = False
        self.header = None
        self.session = rq.Session()
        retry = Retry(
            total=request_retries,
            read=request_retries,
            connect=request_retries,
            backoff_factor=0.1,
            status_forcelist=retry_on_statuses if request_retries > 1 else None,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    @property
    def is_authenticated(self):
        """
        Verify whether this session has an authentication token

        :return:                        True if the session is authenticated, False otherwise
        """
        return self._is_authenticated

    def authenticate(self, username: str, password: str):
        """
        Authenticate to the ETNA API services

        :param username:                the user's login (in the form login_x)
        :param password:                the user's password
        :return:                        a JSON object containing user information

        :raises EtnaAPI.AuthError:      if the authentication is not successful
        """
        login_route = self.auth_url + "/login"
        ret = self.session.post(login_route, json={
            "login": username,
            "password": password,
        })
        if ret.status_code != 200:
            raise AuthError("Unable to login as " + username + ": code " + str(ret.status_code))
        elif "set-cookie" not in ret.headers:
            raise AuthError("Unable to login as " + username + ": no auth token was received")
        self.header = {"Cookie": ret.headers["set-cookie"]}
        self._is_authenticated = True
        return ret.json()

    def identity(self):
        """
        Query the API for the user's information

        :return:                        a JSON object containing user information

        :raises EtnaAPI.AccessDenied:   if the user is not logged in
        """
        identity_route = self.auth_url + "/identity"
        resp = self.session.get(identity_route, headers=self.header)
        if resp.status_code == 401:
            raise AuthorizationRequired("You are not logged in !")
        return resp.json()
