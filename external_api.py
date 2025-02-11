import xmlrpc.client

url = "http://localhost:9001/"
db = "sample_database_1"
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

print(common.version())
print(uid)

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

fields = models.execute_kw(db, uid, password, 'hospital.patient', 'fields_get', [],
                           {'attributes': ['string', 'help', 'type']})
print(fields)

ids = models.execute_kw(db, uid, password, 'hospital.patient', 'search', [[['patient_name', '=', 'abc']]])
print(ids)
users = models.execute_kw(db, uid, password, 'hospital.patient', 'read', [ids], {'fields': ['name']})
print(users)

user = models.execute_kw(db, uid, password, 'hospital.patient', 'search_read', [[['gender', '=', 'male']]],
                         {'fields': ['patient_name', 'email', 'date_of_birth'], 'limit': 5})
print(user)

id = 8
update = models.execute_kw(db, uid, password, 'hospital.patient', 'write',
                           [[id], {'patient_name': "Newer partner", "state": 'inactive'}])
ids = models.execute_kw(db, uid, password, 'hospital.patient', 'search_read', [[['id', '=', 8]]],
                        {'fields': ['patient_name', 'email', 'date_of_birth']})
print(ids)

id = models.execute_kw(db, uid, password, 'hospital.speciality', 'create', [{"name": "ajanjsnscasjcioas"}])
print(id)
