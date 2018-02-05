## 62:	Profit is its own reward. The riskier the config file, the greater the profit.

DEBUG = False

BENCHMARK_RESULT_FILE = 'bench.json' # persistent json that will store the hashrate achieved by the different miners to assist with profit calculations
MINER_DIR = 'miners' # the directory that holds all the miner executables and their associated library files, etc

WORKER = 'dogs_are_cool' # worker name for all miners

DIAG_INTERVAL = 30  # how often to check miners, print info, in seconds
EVALUATE_INTERVAL = 2700 # how often to check WhatToMine and switch coins if needed (also seconds)
WATCHDOG_TIMEOUT = 2 # how many DIAG_INTERVAL of 0 hashrate should pass before the miner is considered not working
SOCKET_TIMEOUT = 2 # timeout for local API calls

# miningpoolhub creds
MPH_URL = 'hub.miningpoolhub.com' # one url for all pools
MPH_USER = 'dogetorhue' # login username (need an account)
MPH_PASS = 'x' # no reason to change this from 'x'
# nicehash creds
NH_URL = '{algo}.usa.nicehash.com' # formatted to the specific algo
NH_ADDRESS = '1HJc8bjpJvogYfXdCNGg8NScN49M6JVDe5' # bitcoin address until they change that
NH_PASSWORD = 'x' # also constant

WTM_EXCHANGES = ['bittrex','poloniex','yobit'] # these are the exchanges that MPH uses
WTM_JSON_URL = "https:/whattomine.com/coins.json" # WtM api url
WTM_JSON_PAYLOAD = {'sort':'Profitability24', 'revenue':'24h', 'factor[cost]':0, 'factor[exchanges][]':WTM_EXCHANGES} # the constant api payload that is appended to the hashrates (which are generated later)


if DEBUG: # makes it easy to switch to a mode for debugging
	LOG_LEVEL_PRINT = 2 # how high priority messages need to be for printing to command line
	LOG_LEVEL_FILE = 1 # same, level to be saved to log file
	LOG_FILE = 'optimine.log' # this file will be overwritten every time the program restarts
	LOG_TO_FILE = True # if False, does not write a log file
else: # if not in debug mode, no log file is used
	LOG_LEVEL_PRINT = 3
	LOG_LEVEL_FILE = 0
	LOG_FILE = ''
	LOG_TO_FILE = False
