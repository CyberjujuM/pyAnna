from module import Module

class Compteur(Module):
	def __init__(self, room):
		self.room = room

	def update_nb_participants(self):
		nb_participants = len(self.room.get_roster())
		f = open('compteur_' + self.room.get_roomname(), 'w')
		f.write(str(nb_participants))
		f.close()

	def muc_online(self, presence):
		self.update_nb_participants()

	def muc_offline(self, presence):
		self.update_nb_participants()
