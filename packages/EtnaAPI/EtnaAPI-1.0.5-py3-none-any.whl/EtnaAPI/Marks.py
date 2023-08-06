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

    def get_marks(self, group_id: int):
        resp = self.session.get(self.module_api + "/" + self._activity_url + "/checklist/group/" + str(group_id),
                                headers=self.session.header)
        if resp.status_code == 401:
            raise EtnaAPI.AuthorizationRequired("Authorization required")
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to get marks for group {} in activity {}: access denied"
                                       .format(group_id, self.activity_id))
        elif resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to get marks for group {} in activity {}: not found"
                                   .format(group_id, self.activity_id))
        elif resp.status_code == 400:
            raise EtnaAPI.BadRequest("Unable to get marks for group {} in activity {}: bad request"
                                     .format(group_id, self.activity_id))
        return resp.json()

    def update_marks(self, group_id: int, data):
        resp = self.session.post(self.module_api + "/" + self._activity_url + "/checklist/group/" + str(group_id),
                                 headers=self.session.header,
                                 json=data)
        if resp.status_code == 401:
            raise EtnaAPI.AuthorizationRequired("Authorization required")
        if resp.status_code == 403:
            raise EtnaAPI.AccessDenied("Unable to update marks for group {} in activity {}: access denied"
                                       .format(group_id, self.activity_id))
        elif resp.status_code == 404:
            raise EtnaAPI.NotFound("Unable to update marks for group {} in activity {}: not found"
                                   .format(group_id, self.activity_id))
        elif resp.status_code == 400:
            raise EtnaAPI.BadRequest("Unable to update marks for group {} in activity {}: bad request"
                                     .format(group_id, self.activity_id))
        return resp.json()
