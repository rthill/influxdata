#!/usr/bin/env python3
#########################################################################
#  Copyright 2015 Raoul Thill                       raoul.thill@gmail.com
#########################################################################
#  This file is part of SmartHome.py.    http://mknx.github.io/smarthome/
#
#  SmartHome.py is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHome.py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHome.py. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import logging
import socket

logger = logging.getLogger('')


class InfluxData:
    def __init__(self, smarthome, influx_host='localhost', influx_port=8089, influx_keyword='influx'):
        logger.warn('Init InfluxData')
        self._sh = smarthome
        self.influx_host = influx_host
        self.influx_port = influx_port
        self.influx_keyword = influx_keyword
        self._items = []

    def run(self):
        self.alive = True

    def stop(self):
        self.alive = False

    def udp(self, data):
        try:
            family, type, proto, canonname, sockaddr = socket.getaddrinfo(self.influx_host, self.influx_port)[0]
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data.encode(), (sockaddr[0], sockaddr[1]))
            sock.close()
            del sock
        except Exception as e:
            logger.warning(
                    "InfluxData: Problem sending data to {}:{}: {}".format(self.influx_host, self.influx_port, e))
            pass
        else:
            logger.debug("InfluxData: Sending data to {}:{}: {}".format(self.influx_host, self.influx_port, data))

    def parse_item(self, item):
        if self.influx_keyword in item.conf:
            if item.type() not in ['num', 'bool']:
                logger.debug("InfluxData: only supports 'num' and 'bool' as types. Item: {} ".format(item.id()))
                return
            self._items.append(item)
            return self.update_item

    def update_item(self, item, caller=None, source=None, dest=None):
        message = "{},caller={},source={},dest={} value={}".format(item.id(), caller, source, dest, float(item()))
        self.udp(message)
        return None

    def _update_values(self):
        return None
