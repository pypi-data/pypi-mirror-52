from pythonfiledatastore import main_executor 
from pythonfiledatastore import operations
import argparse

class datastore():
	
	def __init__(self, args):
		self.key = args.get('key', None)
		self.value = args.get('value', None)
		self.client = args.get('client', None)
		self.ttl = args.get('ttl', None)

	
	def create(self):
		if self.ttl:
			return main_executor.create(self.client, self.key, self.value, ttl = int(self.ttl))
		else:
			return main_executor.create(self.client, self.key, self.value)


	def read(self):
		return main_executor.read(self.client, self.key)


	def delete(self):
		return main_executor.delete(self.client, self.key)


	def reset(self):
		return main_executor.reset(self.client)


def datastore_invoke(operation_name, **kwargs):

	operation = operation_name
	datastore_app = datastore(kwargs)
	status = ""

	if operation == 1:
		status = datastore_app.create()
	elif operation == 2:
		status = datastore_app.read()
	elif operation == 3:
		status = datastore_app.delete()
	elif operation == 4:
		status = datastore_app.reset()
	else:
		status = "Operation Not Found" + "Operation_name  1 - Create (--client --key  --ttl(optional) --value) | 2 - Read (--client --key) | 3 - Delete (--client --key) | 4 - Reset (--client)"

	return status



if __name__ == "__main__": 
	
	parser = argparse.ArgumentParser()

	parser.add_argument("-k", "--key",help="Input Key")
	parser.add_argument("-v", "--value",help="Input Value")
	parser.add_argument("-c", "--client",help="client_file_name")
	parser.add_argument("-t", "--ttl",help="optional Time to live for Key(seconds)")
	parser.add_argument("-o", "--operation",help="Operation_name  1 - Create (--client --key  --ttl(optional) --value) | 2 - Read (--client --key) | 3 - Delete (--client --key) | 4 - Reset (--client)")

	args = parser.parse_args()
	client = args.client
	key = args.key
	value = args.value
	ttl = args.ttl

	operation = int(args.operation)

	print(datastore_invoke(operation, client = client, key = key, value = value, ttl = ttl))

