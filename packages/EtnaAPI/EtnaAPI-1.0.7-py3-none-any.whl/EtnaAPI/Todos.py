#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests as rq
import EtnaAPI


class Controller(EtnaAPI.BasicController):
    def get_todo(self, ticket_id: int):
        """
        Get information about a ticket given its ID

        :param ticket_id:               the ticket ID, as a number

        :return:                        a dictionary containing the ticket information
        """
        res = self.req_session.get("https://tickets.etna-alternance.net/api/todos/" + str(ticket_id) + ".json",
                                   headers=self.session.header)
        if res.status_code == 401:
            raise EtnaAPI.AuthorizationRequired("Authorization required")
        if res.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get ticket with ID {}: access denied".format(ticket_id))
        if res.status_code == 404:
            raise EtnaAPI.NotFound("Unable to get ticket with ID {}: not found".format(ticket_id))
        return res.json()['data']

    def update_todo(self, ticket_id: int, todo):
        """
        Update an existing ticket

        :param ticket_id:               the ticket ID, as a number
        :param todo:                    a dictionary containing the information to set for the ticket

        :return:                        a dictionary containing the ticket information after the update

        :raises EtnaAPI.EtnaAPIError:   if the ticket could not be updated
        """
        resp = self.req_session.put("https://tickets.etna-alternance.net/api/todos/" + str(ticket_id) + ".json",
                                    json=todo, headers=self.session.header)
        if resp.status_code != 200:
            raise EtnaAPI.EtnaAPIError("Unable to update the ticket")
        return resp.json()['data']

    def create_todo(self, todo):
        """
        Create a new ticket

        :param todo:                    a dictionary containing the information for the ticket to be created

        :return:                        a dictionary containing the newly-created ticket information

        :raises EtnaAPI.EtnaAPIError:   if the ticket could not be created
        """
        resp = self.req_session.post("https://tickets.etna-alternance.net/api/todos.json",
                                     json=todo, headers=self.session.header)
        if resp.status_code != 201:
            raise EtnaAPI.EtnaAPIError("Unable to create the ticket")
        return resp.json()['data']
