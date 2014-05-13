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
import sys

from glastopf.modules.handlers import base_emulator
from glastopf.modules.handlers.base_emulator import package_directory


logger = logging.getLogger(__name__)

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

class ImageContent(base_emulator.BaseEmulator):
    def __init__(self, data_dir):
        super(ImageContent, self).__init__(data_dir)

    def handle(self, attack_event):
        server_path = os.path.join(package_directory, 'emulators/data/images')
        request_file = attack_event.http_request.request_path.rsplit('/',1)[-1]
        logger.info('Serving image file %s' % (os.path.join(server_path,request_file),))
        # attack_event.http_request.set_response('',headers=('Content-type: image/jpeg\n\n',))
        if os.path.isfile(os.path.join(server_path, request_file)):
            with open(os.path.join(server_path, request_file), 'rb', 0) as f:
                response = f.read()
        # attack_event.http_request.set_raw_response(response)
        attack_event.http_request.set_response(response,headers=(('Content-type','image/jpeg'),))
        return attack_event
