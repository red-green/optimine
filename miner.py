## 208:	Sometimes the only thing more dangerous than a question is an answer. (to the query for your GPU temperature)

import subprocess, shlex, os, sys, socket
from config import *

class miner:
	def __init__(self,coin,benchmark=False):
		self.coin = coin
		self.benchmark_mode = benchmark
		if not coin in COINS.keys():
			log(6,'the coin {} was not found in the config file!'.format(coin))
			exit(1)

		coin_def = COINS.get(self.coin)
		try:
			self.algo = coin_def.get('algo') # algorithm that the coin uses
			stratum_info = coin_def.get('stratum')
			self.stratum_url = stratum_info.get('url') # stratum creds
			self.stratum_port = int(stratum_info.get('port'))
			self.stratum_user = stratum_info.get('user')
			self.stratum_pass = stratum_info.get('pass')
			assert self.algo and self.stratum_url and self.stratum_port and self.stratum_user and self.stratum_pass
		except (AssertionError, AttributeError, ValueError):
			log(6,'improperly formatted config entry for coin {}'.format(coin))
			exit(1)

		algo_def = MINERS.get(self.algo)
		try:
			self.miner_exe = algo_def.get('cmd') # miner executable file
			self.miner_auth = algo_def.get('auth') # args that authenticate the miner
			self.miner_params = algo_def.get('args') # settings that include enabling api and tuning miner
			self.miner_bench = algo_def.get('bench_args') # args to add if the miner is set in benchmark mode
			api_info = algo_def.get('api')
			self.has_api = api_info.get('has_api') # if the miner has an RPC api that can get info about the rates
			if self.has_api:
				self.api_port = int(api_info.get('port')) # no url because it always runs on localhost
				self.api_request = api_info.get('request') # text sent to API that triggers a status response
				self.api_parser = api_info.get('parser') # defines how the api responses are decoded (may want to change to a lambda)
				self.api_hash_func = api_info.get('get_hash') # pass in the parsed api result to these lambdas
				self.api_acc_func = api_info.get('get_accepted')
				self.api_rej_func = api_info.get('get_rejected')
				assert self.api_port and self.api_parser and self.api_hash_func and self.api_acc_func and self.api_rej_func
			else: # otherwise we scrape the stdout with regex
				## TODO: implement regex scraping if the miner lacks an API
				log(4,'the miner {} lacks an API and regex scraping is not yet implemented')
				pass
			assert self.miner_exe and self.miner_auth and self.miner_params and self.miner_bench
		except (AssertionError, AttributeError, ValueError):
			log(6,'improperly formatted config entry for miner {}'.format(self.algo))
			exit(1)

		## start assembling the commands
		self.launch_cmd = []
		self.launch_cmd.append(self.miner_exe) # may want to do something about the relative directories
		if self.benchmark_mode:
			self.launch_cmd += shlex.split(self.miner_bench)
		else: # if benchmarking, we skip authentication
			auth_args = self.miner_auth.format(stratum=self.stratum_url, port=self.stratum_port, user=self.stratum_user, passwd=self.stratum_pass, worker=WORKER)
			self.launch_cmd += shlex.split(auth_args)
		self.launch_cmd += shlex.split(self.miner_params)
		log(2,'miner command assembled:')
		log(2,' '.join(self.launch_cmd))

		self.is_running = False # different states that govern behavior within controller
		self.is_warming_up = False
		self.is_stopping = False
		self.is_finished = False

		self.process = None # points to subprocess.Popen class

		self.last_hashrate = -1 # used for calculating the rates used in benchamrks
		self.average_hashrate = -1

		self.stat_hashrate = 0 # these should be used by external stuff reading the info
		self.stat_accepted = 0
		self.stat_rejected = 0

		self.process_out_buffer = '' # buffers for reading miner prints
		self.process_err_buffer = ''


	def start(self):
		try:
			log(1,'beginning to start the miner...')
			self.process = subprocess.Popen(self.launch_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=MINER_DIR, universal_newlines=True)
			self.is_running = True
			self.is_warming_up = True
			log(2,'successfully launched miner')
		except (ValueError,):
			log(6,'the miner could not be started')
			exit(6)
		except (OSError,):
			log(6,'the miner executable could not be found')
			exit(6)


	def check(self):
		stdout,stderr = self.process.communicate()
		if stdout:
			self.process_out_buffer += stdout
		if stderr:
			self.process_err_buffer += stderr
		lines_to_scrape = []
		while '\n' in self.process_out_buffer:
			line,self.process_out_buffer = self.process_out_buffer.split('\n',1)
			log(1,'[miner:] '+line)
			## process the line if needed (i.e. scrape hashrate)
		while '\n' in self.process_err_buffer:
			line,self.process_err_buffer = self.process_err_buffer.split('\n',1)
			log(2,'[miner err:] '+line)
			## same with stderr
		if self.has_api:
			self.read_stats_api()
		else:
			self.read_stats_buff(lines_to_scrape)
		## also log hashrate
		ret = self.process.poll()
		if ret is None: # still running
			return True
		else:
			return False

	def stop(self):
		# tells the miner to stop
		self.process.terminate()

	def read_stats_api(self): ## used internally
		try:
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			sock.settimeout(SOCKET_TIMEOUT)
			sock.connect(('localhost',self.api_port))
			sock.sendall(self.api_request)
