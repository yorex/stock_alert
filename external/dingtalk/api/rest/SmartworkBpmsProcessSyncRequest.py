'''
Created by auto_sdk on 2019.07.03
'''
from dingtalk.api.base import RestApi
class SmartworkBpmsProcessSyncRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.agent_id = None
		self.biz_category_id = None
		self.process_name = None
		self.src_process_code = None
		self.target_process_code = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.smartwork.bpms.process.sync'
