#  Copyright 2018 Kristi Nikolla
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import functools
import json
import math
import requests

from pysamlds import config


@functools.lru_cache()
def fetch_entities():
    r = requests.get(config.DISCOFEED)
    idp_list = json.loads(r.text)
    idps = {}
    for idp_ref in idp_list:
        idp = IdentityProvider(idp_ref)
        idps[idp.entity_id] = idp
    return idps


class IdentityProvider(object):
    """
     "entityID": "",
     "DisplayNames": [
      {
      "value": "Name",
      "lang": "2 char name of lang"
      },
     ],
     "Logos": [
      {
      "value": "url or encoding",
      height": "x",
      "width": "y"
      }
     ]
    }
    """
    def __init__(self, idp_ref):
        self.entity_id = idp_ref['entityID']
        self.name = self.get_name(idp_ref)
        self.logo = self.get_logo(idp_ref)

    @staticmethod
    def get_name(idp_ref):
        for name in idp_ref['DisplayNames']:
            if name['lang'] == 'en':
                return name['value']
        return ''

    @staticmethod
    def get_logo(idp_ref):
        delta_x = math.inf
        result = None
        for logo in idp_ref.get('Logos', {}):
            value = logo['value']  # type: str
            if value.startswith('http'):
                new_delta = abs(config.TARGET_LOGO_WIDTH - int(logo['width']))
                if new_delta < delta_x:
                    result = value
            else:
                return value
        return result
