from Classes.GlobalConfig import globalConfig 
import requests
import json 
from algator_global import IS_PRODUCTION

class ServerConnector(object):

  def talkToServer(self, request):    
    globalConfig.logger.info("REQUEST: " + request)

    try:
      (name, port) = globalConfig.getALGatorServerConnectionData()
      headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}

      parts = request.split(' ')
      url = f"http://{'s' if IS_PRODUCTION else ''}" + name + ":" + str(port) + "/" + parts[0]
      parts = parts[1:] 
      data  = ' '.join(parts)
      encoded_data = data.encode("utf-8")

      response = requests.post(url, data=encoded_data, headers=headers, verify=IS_PRODUCTION)

      return response.text

    except Exception as e:
      return json.dumps({"answer":"TalkToServer error: " + repr(e)})

connector = ServerConnector()
