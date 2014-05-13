# Copyright (C) 2014 Mitch Patenaude
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import logging
import os

from glastopf.modules.handlers import base_emulator
from glastopf.modules.handlers.base_emulator import package_directory


logger = logging.getLogger(__name__)

class StaticContent(base_emulator.BaseEmulator):
    def __init__(self, data_dir):
        super(StaticContent, self).__init__(data_dir)

    def handle(self, attack_event):
        server_path = os.path.join(package_directory, 'emulators/data/static')
        request_file = attack_event.http_request.request_path.lstrip('/')
        if request_file == "":
            request_file = "index.html"
        # logger.info('Serving static file %s' % (os.path.join(server_path,request_file),))
        response = ''
        if os.path.isfile(os.path.join(server_path, request_file)):
            with open(os.path.join(server_path, request_file), 'r') as f:
                response += f.read()
        attack_event.http_request.set_response(response)
        return attack_event
