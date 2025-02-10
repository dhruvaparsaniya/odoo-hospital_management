import xmlrpc.client

url = "http://localhost:9001/"
db = "sample_database_1"
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
