import base64
import codecs
from odoo import http
from odoo.http import request
import pdb
class Hospital(http.Controller):

    @http.route('/patient_webform',website = True ,auth='public' ,type="http")
    def patient_register(self,**kwarg):
        return request.render("Hospital1.create_patient",{})
        # return "hello"

    @http.route('/create/patient',website = True ,auth='public' ,type='http')
    def create_patient(self,**kwarg):
        # pdb.set_trace()
        print("before creation -------------",kwarg)
        encoded_img=kwarg.get('image').encode()
        kwarg.update(image=base64.b64encode(encoded_img))
        request.env['hospital.patient'].sudo().create(kwarg)
        print("after creation -------------",kwarg)
        return request.render("Hospital1.patient_tankyou",{})