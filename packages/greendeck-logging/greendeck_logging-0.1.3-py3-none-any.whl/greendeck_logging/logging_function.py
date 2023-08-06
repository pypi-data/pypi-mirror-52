import json

def message_value(message, info, value):
	counter_message = {}
	counter_message ['counter_message'] = message
	counter_message['counter_value'] = value
	
	if info != {}:
		if info is not None and type(info) == type({}):
			counter_info =  info
			try:
				counter_info_str = json.dumps(counter_info)
				counter_message['info'] = counter_info
			except Exception as e:
				print("GDLOGGING : please provide info as dict")
				print(str(e))
				pass

	return counter_message
