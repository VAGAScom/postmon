#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from airbrake.notifier import Airbrake


class AirbrakePostmon(object):

    def __init__(self):
        PROJECT_ID = os.environ.get('AIRBRAKE_PROJECT_ID', 1234)
        API_KEY = os.environ.get('AIRBRAKE_API_KEY', 'fake')
        ENVIRONMENT = os.environ.get('AIRBRAKE_ENVIRONMENT', 'dev')

        self._ab = Airbrake(project_id=PROJECT_ID,
                            api_key=API_KEY,
                            environment=ENVIRONMENT)

    def notify(self, message):
        self._ab.notify(message)
