import json


def validate_dictionary_value(data_dict):
	for key, value in data_dict:
		try:
			if value.strip():
				del data_dict[key]
		except:
			if value == None:
				del data_dict[key]
	
	return data_dict

def message_value(message, info, value):
	counter_message = {}
	counter_message ['counter_message'] = message
	counter_message['counter_value'] = value
	
	if info != {}:
		if info is not None and type(info) == type({}):
			counter_info =  info
			try:
				counter_info_str = json.dumps(counter_info)
				counter_info = json.loads(counter_info_str)

			except Exception as e:
				print("GDLOGGING : please provide info as dict")
				print(str(e))
				pass
	
	counter_info = validate_dictionary_value(counter_info)
	counter_message['info'] = counter_info
	return counter_message
