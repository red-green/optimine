## 17:	A contract is a contract is a contract... but only once it has been confirmed on the blockchain.

from config import *
from miner_controllers import *
from definitions import *

class mph_stratum(stratum): # miningpoolhub has all their stratums at one address, only changing the port
	def __init__(self,port):
		super(mph_stratum,self).__init__(MPH_URL,port,MPH_USER,MPH_PASS) # pulled from config

class nh_stratum(stratum): # nicehash can also be abstracted a bit
	def __init__(self,algo,port):
		super(mph_stratum,self).__init__(NH_URL.format(algo=algo),port,NH_ADDRESS,NH_PASS)

ALGOS = {}
MINERS = {}
COINS = {}

# algorithms
ALGOS['equihash'] = equihash = algorithm('equihash','eq','eq')
ALGOS['lyra2rev2'] = lyra2rev2 = algorithm('lyra2rev2','lre','lrev2')
ALGOS['neoscrypt'] = neoscrypt = algorithm('neoscrypt','ns','ns')

# miners (not controllers)
MINERS['nheqminer'] = nheqminer = miner('nheqminer',equihash,nheq_controller,[])
MINERS['excavator_neoscrypt'] = excavator_neoscrypt = miner('excavator_neoscrypt',neoscrypt,excavator_controller,{'algo':'neoscrypt'})

# coins
COINS['zcash'] = zcash = coin('zcash',nheqminer,mph_stratum(20570)) # mph equihash
COINS['zclassic'] = zclassic = coin('zclassic',nheqminer,mph_stratum(20594))
COINS['zencash'] = zencash = coin('zencash',nheqminer,mph_stratum(20575))
COINS['bitcoingold'] = bitcoingold = coin('bitcoingold',nheqminer,mph_stratum(20595),'BitcoinGold')

COINS['nh_equihash'] = nh_equihash = coin('nh_equihash',nheqminer,nh_stratum('equihash',3357),'Nicehash-Equihash') # nh algo rental
COINS['nh_neoscrypt'] = nh_neoscrypt = coin('nh_neoscrypt',excavator_neoscrypt,nh_stratum('neoscrypt',3341),'Nicehash-NeoScrypt')
