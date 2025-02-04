from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class hospital_physician(models.Model):
    _name="hospital.physician"
    _description="physician data"
    _rec_name = 'physician_name'
    _inherits = {"res.users": "usuario_id"}

    usuario_id = fields.Many2one(
        "res.users", required=True, ondelete="restrict", auto_join=True
    )
    physician_id = fields.Char("physician id",default='new',readonly=True)
    physician_name=fields.Char("Name",required=True)
    email=fields.Char("Email",required=True)
    physician_specialty=fields.Many2many("hospital.speciality",required=True)

    @api.constrains('pysician_name','email')
    def validate_constrains(self):
        pattern_name=r'[a-zA-Z ]{2,}'
        validate_name=re.match(pattern_name,self.physician_name)
        if validate_name == None:
            raise ValidationError("Invalid name...please enter correct Name(name should not cotain any number).")

        pattern=r'^[a-z0-9-._]*@[a-z0-9-]*(\.[a-z]{2,4})$'
        validate=re.match(pattern,self.email)
        if validate == None:
            raise ValidationError("Invalid email...please enter correct email.(formate:_____@__.__)")

    @api.model
    def create(self,vals):
        vals['physician_id'] = self.env['ir.sequence'].sudo().next_by_code("physician.data") or 'New'
        vals['name']=vals.get("physician_name")
        vals['login']=vals.get("email")
        return super(hospital_physician, self).create(vals)