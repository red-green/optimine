## 109:	Dignity and an empty server rack is worth the rack.


# this file it just for data structures for defining what coins to mine and how to mine them. this is used in miner_conf.py to actually configure the program
from config import *
from logging import log

class stratum:
	def __init__(self,url,port,user,passwd='x'):
		self.url = url
		self.port = port
		self.user = user
		self.passwd = passwd
		self.worker = WORKER

	def format(self,fstr): # format string for command line stratum input
		return fstr.format(stratum=self.url,port=self.port,user=self.user,port=self.port,passwd=self.passwd)


class algorithm: # algo specific info
	def __init__(self,name,wtm_en,wtm_id):
		self.name = name
		self.wtm_enable = wtm_en # url flag that enables calculation for this algo
		self.wtm_hashid = wtm_id # url flag that passes hashrate for this algo # whattomine did not make these the same for some algos D:
		self.miners = []

	def add_miner(self,miner):
		self.miners.append(miner)

class miner: # miner linking class
	def __init__(self,name,algo,controller,params):
		self.name = name
		self.algo = algo
		self.controller = controller
		self.params = params
		self.algo.add_miner(self)

class coin: # coin specific info
	def __init__(self,name,miner,stratum,wtm_name=None):
		self.name = name
		self.miner = miner
		self.algo = miner.algo
		self.stratum = stratum
		if wtm_name:
			self.wtm_name = wtm_name
		else:
			self.wtm_name = name.capitalize()



class coin_wtm: # defining the data structure of the returned info parsed from whattomine
	def __init__(self,name,algo,profit24):
		self.name = name
		self.algo = algo
		self.profit24 = profit24  # in btc
	def __init__(self,name,coin_json):
		try:
			self.name = WTM_NAMES.get(name)
			self.algo = coin_json.get('algorithm').lower()
			self.profit24 = float(coins_json.get('btc_revenue24'))
		except ValueError:
			return
