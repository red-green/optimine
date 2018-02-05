## 23:	Nothing is more important than your equipment's health... except for your money.

import json, requests, os, sys
from logging import log
from definitions import coin_wtm
from config import *


def load_hashrates():
	if not (os.path.exists(BENCHMARK_RESULT_FILE) and os.isfile(BENCHMARK_RESULT_FILE)):
		log(2,'the benchmark file does not exist')
		return {}
	fd = open(BENCHMARK_RESULT_FILE,'r')
	data = fd.read()
	fd.close()
	if data:
		try:
			algo_json = json.loads(data)
		except ValueError:
			log(3,'improperly formatted benchmark file')
			return {}
		if isinstance(algo_json,dict):
			return algo_json
		else:
			log(3,'improperly formatted benchmark file')
			return {}
	else:
		log(2,'the benchmark file is empty')
		return {}

def update_hashrate(algo,rate):
	log(2,'updating the benchmark for {} to {}'.format(algo,rate))
	last_rates = load_hashrates()
	try:
		fd = open(BENCHMARK_RESULT_FILE,'w')
		last_rates[algo] = rate
		new_data = json.dumps(last_rates)
		fd.write(new_data)
		fd.close()
	except:
		log(5,'error saving benchmark file')

'''
def generate_wtm_url():
	hashrates = load_hashrates()
	hashrate_enc = []
	for algo in WTM_IDS.keys():
		rate = hashrates.get(algo,-1)
		wid = WTM_IDS.get(algo)
		hashrate_enc.append(WTM_HASH_FORMAT.format(algo=wid,rate=rate))
	formatted = '&'.join(hashrate_enc)
	url = WTM_JSON_URL.format(hashrates=formatted)
	return url
'''

def generate_wtm_payload():
	hashrates = load_hashrates()
	hashrate_enc = {}
	for algo in MINERS.keys():
		if algo in hashrates.keys():
			enable_key = MINERS[algo]['wtm_en']  # why did WTM have to make these different keys???
			hashrate_key = MINERS[algo]['wtm_id']
			hashrate_enc[enable_key] = 'true'
			hashrate_enc['factor[{algo}_hr]'.format(algo=hashrate_key)] = hashrates.get(algo,0)
	return hashrate_enc

def get_wtm_profitibility():
	bench_payload = generate_wtm_payload()
	coins = []
	try:
		request = requests.get(WTM_JSON_URL,payload=bench_payload+WTM_JSON_PAYLOAD)


def find_best_coin():
	profs = get_wtm_profitibility()
