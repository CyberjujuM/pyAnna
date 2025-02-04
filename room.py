# Copyright (C) 2011 - pyAnna
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details at
# http://www.gnu.org/copyleft/gpl.html
# 
# You should have received a copy of the GNU General Public License 
# along with this program; if not, see <http://www.gnu.org/licenses>.
#

from modules.talkative import Talkative
from modules.whois import Whois
from modules.bonjour import Bonjour

class Room:
	def __init__(self, xmpp, room, modules, botname):
		self._xmpp = xmpp
		self._room = room
		self._botname = botname

		self._modules = []
		for module in modules:
			m = module.split(".")
			c = getattr(__import__("modules." + m[0], fromlist=[m[1]]), m[1])
			self._modules.append(c(self))
	
	def connect(self):
		self._xmpp.plugin['xep_0045'].joinMUC(self._room, self._botname)
		self._xmpp.add_event_handler("muc::%s::message" % self._room,
											                               self.handle_message)

		self._xmpp.add_event_handler("muc::%s::got_online" % self._room,
																												 self.muc_online)

	def muc_online(self, presence):
		if presence['muc']['nick'] != self._botname:
			for module in self._modules:
				module.muc_online(presence)

	def handle_message(self, msg):
		if msg['mucnick'] != self._botname:
			for module in self._modules:
				module.handle_message(msg)

	def handle_private_message(self, msg, to):
		if msg['mucnick'] != self._botname:
			for module in self._modules:
				module.handle_private_message(msg, to)

	def get_roster(self):
		return self._xmpp.plugin['xep_0045'].getRoster(self._room)

	def get_jid(self, nick):
		return self._xmpp.plugin['xep_0045'].getJidProperty(self._room, nick, 'jid')

	def get_roomname(self):
		return self._room

	def get_botname(self):
		return self._botname

	def send_message(self, message):
		self._xmpp.send_message(mto=self._room,
														mbody=message,
														mtype='groupchat')


	def send_private_message(self, message, to):
		self._xmpp.send_message(mto=to,
														mbody=message,
														mtype='chat')
