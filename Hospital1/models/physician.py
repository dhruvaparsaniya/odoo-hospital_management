from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re


class hospital_physician(models.Model):
    _name = "hospital.physician"
    _description = "physician data"
    _rec_name = 'physician_name'
    _inherits = {"res.users": "usuario_id"}

    usuario_id = fields.Many2one(
        "res.users", required=True, ondelete="restrict", auto_join=True
    )
    physician_id = fields.Char("physician id", default='new', readonly=True)
    physician_name = fields.Char("Name", required=True)
    email = fields.Char("Email", required=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")])
    mobile_number = fields.Char("Mobile no.")
    physician_specialty = fields.Many2many("hospital.speciality", required=True)

    @api.constrains('pysician_name', 'email', 'mobile_number')
    def validate_constrains(self):
        pattern_name = r'[a-zA-Z ]{2,}'
        validate_name = re.match(pattern_name, self.physician_name)
        if not validate_name:
            raise ValidationError("Invalid name...please enter correct Name(name should not cotain any number).")

        pattern = r'^[a-z0-9-._]*@[a-z0-9-]*(\.[a-z]{2,4})$'
        validate = re.match(pattern, self.email)
        if not validate:
            raise ValidationError("Invalid email...please enter correct email.(formate:_____@__.__)")

        # Validate mobile number
        pattern_mobile = r"^\d{10}$"
        if not re.match(pattern_mobile, self.mobile_number):
            raise ValidationError("Invalid mobile number. Please enter a 10-digit number.")

    @api.model
    def create(self, vals):
        vals['physician_id'] = self.env['ir.sequence'].sudo().next_by_code("physician.data") or 'New'
        vals['name'] = vals.get("physician_name")
        vals['login'] = vals.get("email")
        return super(hospital_physician, self).create(vals)
