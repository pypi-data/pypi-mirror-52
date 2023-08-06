#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests as rq
import EtnaAPI


class Controller(EtnaAPI.BasicController):
    def __init__(self, session: EtnaAPI.Session, module_id: int, activity_id: int):
        super(Controller, self).__init__(session)
        self.module_id = module_id
        self.activity_id = activity_id
        self._activity_url = str(module_id) + "/activities" + "/" + str(activity_id)

    def get_circles(self):
        """
        Retrieve circles information for the activity

        :return:                        a list containing the names of the circles

        :raises EtnaAPI.AccessDenied:   if the user does not have the required permissions
        :raises EtnaAPI.NotFound:       if the module or activity cannot be found
        """
        resp = self.session.get(self.module_api + "/" + self._activity_url + "/conversations/circles",
                      headers=self.session.header)
        if resp.status_code == 401:
            raise EtnaAPI.AuthorizationRequired("Authorization required")
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get conversations for activity {}: access denied"
                                       .format(self.activity_id))
        elif resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to get marks for activity {}: not found".format(self.activity_id))
        return resp.json()

    def add_conversation_for_activity(self, data):
        """
        Add a new conversation for the given activity
        """
        resp = self.session.post(self.module_api + "/" + self._activity_url + "/conversations", json=data,
                       headers=self.session.header)
        if resp.status_code == 401:
            raise EtnaAPI.AuthorizationRequired("Authorization required")
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get conversations for activity {}: access denied"
                                       .format(self.activity_id))
        elif resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to get marks for activity {}: not found".format(self.activity_id))
        return resp.json()
