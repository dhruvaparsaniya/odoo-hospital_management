import base64
from odoo import http
from odoo.http import request
import pdb
class Hospital(http.Controller):

    @http.route('/patient_webform',website = True ,auth='public' ,type="http")
    def patient_register(self,**kwarg):
        return request.render("Hospital1.create_patient",{})
        # return "hello"

    @http.route('/create/patient',website = True ,type='http',csrf=False)
    def create_patient(self,**kwarg):
        files = request.httprequest.files.getlist('image')
        print("----------------------------------------------------",files)
        for file in files:
            attachment=file.read()
            if attachment:
                # pdb.set_trace()
                kwarg['image'] = base64.b64encode(attachment).decode('utf-8')
                request.env['hospital.patient'].sudo().create(kwarg)

        return request.render("Hospital1.patient_tankyou", {})