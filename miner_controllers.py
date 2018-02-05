## 211:	Miners are the rungs on the ladder of success. Don't hesitate to step on them.

import shlex

class miner_controller: # base class to handle launching and interacting with a CLI miner. however, it is not full-featured, so it must be extended by other classes to handle specific miners
	error = False
	process = None # points to subprocess.Popen class
	process_out_buffer = '' # buffers for reading miner prints
	process_err_buffer = ''

	stratum = None
	def set_stratum(self,stratum):
		self.stratum = stratum

	def launch_proc(self,cmd): # starts the command (must be compiled and split properly first)
		try:
			self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=MINER_DIR, universal_newlines=True)
		except OSError:
			log(6,'the miner executable could not be found')
			exit(6)

	def stop_proc(self):
		if self.process:
			self.process.terminate()

	def communicate(self): # empties buffers and returns a list of lines that have been printed (both out and err)
		stdout,stderr = self.process.communicate()
		if stdout:
			self.process_out_buffer += stdout
		if stderr:
			self.process_err_buffer += stderr
		lines = []
		while '\n' in self.process_out_buffer:
			line,self.process_out_buffer = self.process_out_buffer.split('\n',1)
			log(1,'[miner:] '+line)
			lines.append(line)
		while '\n' in self.process_err_buffer:
			line,self.process_err_buffer = self.process_err_buffer.split('\n',1)
			log(2,'[miner err:] '+line)
			lines.append(line)
		return lines

	def check_running(self): # checks if process has crashed
		if not self.process:
			return False
		ret = self.process.poll()
		if ret is None: # still running
			return True
		else:
			return False

	@property
	def is_running(self): # can be overridden
		return self.check_running()

#################################################

class cli_miner_controller(miner_controller): # to run a single miner that is started with a command and is stopped with a SIGKILL
	pass

class api_miner_controller(miner_controller): # to run a miner that is started by sending API requests to a daemon, which is handled as a singleton process
	pass

#################################################

class excavator_controller(miner_controller):
	# because excavator has multiple algos, it will be implemented with a singleton process and simply stopped when other ones are running
	class cmd_conf:
		cmd = 'excavator/excavator'
		args = '-p {api_port}'
	class api_conf:
		port = 24992

	def __init__(self,params):
		self.algo = params.get('algo')



class nheq_controller(miner_controller):
	pass
