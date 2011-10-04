# Copyright (C) 2011  Lukas Rist
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import modules.HTTP.util as util
import modules.HTTP.method_handler as method_handler
import modules.events.attack as attack
from modules.handlers import request_handler
import modules.reporting.log_sqlite as log_sqlite

class GlastopfHoneypot(object):

    def __init__(self):
        self.sqlite_logger = log_sqlite.LogSQLite()

    def print_info(self, attack_event):
        print attack_event.event_time,
        print attack_event.source_addr[0] + " requested",
        print attack_event.parsed_request.method, 
        print attack_event.parsed_request.url, "on", 
        print attack_event.parsed_request.header["Host"]
    
    def handle_request(self, raw_request, addr):
        HTTP_parser = util.HTTPParser()
        attack_event = attack.AttackEvent()
        # Parse the request
        attack_event.parsed_request = HTTP_parser.parse_request(raw_request)
        attack_event.source_addr = addr
        self.print_info(attack_event)
        # Start response with the server header
        # TODO: Add msg length header
        attack_event.response = util.HTTPServerResponse.response_header
        MethodHandlers = method_handler.HTTPMethods()
        # Handle the HTTP request method
        attack_event.matched_pattern = getattr(MethodHandlers, attack_event.parsed_request.method, "GET")(attack_event.parsed_request)
        # Handle the request with the specific vulnerability module
        getattr(request_handler, attack_event.matched_pattern, request_handler.unknown)(attack_event)
        # Logging the event
        self.sqlite_logger.insert(attack_event)
        return attack_event.response