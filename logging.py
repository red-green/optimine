## 3:	Never spend more for an acquisition than you have to.

from config import *

def log(level,text):
	formatted = str(text)
	if level >= LOG_LEVEL:
		print formatted
