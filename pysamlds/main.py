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

from urllib import parse

from pysamlds import app
from pysamlds import discovery

import flask


@app.app.route('/', methods=['GET'])
def index():
    return_to = flask.request.args.get('return', '')
    if not return_to:
        flask.abort(400)

    idps = discovery.fetch_entities()
    return_to = parse.unquote(return_to)
    return flask.render_template('index.html',
                                 return_to=return_to,
                                 idps=idps.values())


if __name__ == '__main__':
    app.app.run()
