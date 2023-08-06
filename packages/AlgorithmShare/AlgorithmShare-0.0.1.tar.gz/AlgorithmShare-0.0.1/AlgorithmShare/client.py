import requests
from requests.exceptions import ConnectTimeout
import urllib3

class AlgoShareError(Exception):
        def __init__(self, ErrorInfo):
                #super().__init__(self)
                self.errorinfo = ErrorInfo

        def __str__(self):
                return self.errorinfo


class client:
	base_url = 'http://earthdataminer.casearth.cn:30090/'
	def __init__(self):
		self.username = ''
	
	def algo(self, algo_path):
		return algorithm(algo_path)


class item:
	def __init__(self, status_code, result):
		self.status_code = status_code
		self.result = result


class algorithm:
	def __init__(self, algo_path):
		self.algo_path = algo_path
		
	def set_options(self, timeout=300):
		self.timeout = timeout
		
	def pipe(self, input_data):
		request_url = client.base_url+self.algo_path
		try:
			r = requests.post(request_url, data=input_data, timeout=200)
			r.raise_for_status()
		except (urllib3.exceptions.ConnectTimeoutError, ConnectTimeout, urllib3.exceptions.MaxRetryError):
			raise AlgoShareError('连接超时')
		except HTTPError:
			raise AlgoShareError('返回异常')
			return item(r.status_code, 'Error')
		else:
			return item(r.status_code, r.json())
		
		#print (r.json())
		#return item(r.status_code, r.json())
"""
input_data = {'imgfile': 'bird.jpg'}
client = client()
algo = client.algo('1002/casbirdtest/0.1')
print(algo.pipe(input_data).result)
#print(algo.pipe(input_data).status_code)
"""
