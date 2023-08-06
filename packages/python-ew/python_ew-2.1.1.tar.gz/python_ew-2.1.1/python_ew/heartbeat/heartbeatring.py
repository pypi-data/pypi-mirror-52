"""
Heartbeat python interface for Earthworm
Copyright (C) 2013, OSOP SA Panama

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import datetime

from python_ew.heartbeat import heartbeatmodule
from python_ew.tracebuf2 import tracebuf2module
from python_ew.status.statusring import StatusMessage

from python_ew.ring import Ring


#Interface class for Reading/Writing Darien Type message from/into a ring.
class HeartBeatRing(Ring):

    def __init__(self, ring_name, module_id):
        super().__init__(ring_name, module_id, StatusMessage)

    def module_write(self, **args):
        """
        Implementing base class method, simply calling the 'ring_write' function from the tracebuf2module module.
        """
        return tracebuf2module.ring_write(**args)

    def module_read(self, **params):
        raise TypeError("Writing heartbeat type messages is not supported. Use 'beat' instead.")

    def beat(self):
        args = {}
        args = self.completeWriteDict(args)
        args['unix_time'] = str((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())
        self.sequence += 1
        return heartbeatmodule.ring_write(**args)
