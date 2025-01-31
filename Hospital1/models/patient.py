import base64
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError
import re
class hospital_patient(models.Model):
    _name = "hospital.patient"
    _description = "Patient Data"
    _inherits = {"res.users": "usuario_id"}

    usuario_id = fields.Many2one(
        "res.users", required=True, ondelete="restrict", auto_join=True
    )

    patient_name=fields.Char('Name', required=True)
    email=fields.Char('Email',required=True)
    date_of_birth = fields.Date("Date of Birth")
    mobile_number = fields.Char("Mobile no.")
    gov_identity = fields.Char("Gov. ID Number")
    gender = fields.Selection([("male", "Male"), ("female", "Female")])
    patient_age = fields.Char("Age", compute="_compute_age", store=True)
    image=fields.Binary()

    _sql_constraints = [
        ("unique_id", "unique(gov_identity)", "A patient with the same Gov. Identity already exists.")
    ]

    @api.constrains("name", "date_of_birth", "mobile_number", "email", "gov_identity")
    def validate_constraints(self):
        # Validate name
        pattern_name = r"^[a-zA-Z ]{2,}$"
        if not re.match(pattern_name, self.name):
            raise ValidationError("Invalid name. Name should not contain numbers or special characters.")

        # Validate date of birth
        current_date = fields.Date.today()
        if self.date_of_birth and self.date_of_birth >= current_date:
            raise ValidationError("Invalid date of birth. Please enter a correct date.")

        # Validate mobile number
        pattern_mobile = r"^\d{10}$"
        if not re.match(pattern_mobile, self.mobile_number):
            raise ValidationError("Invalid mobile number. Please enter a 10-digit number.")

        # Validate government identity number
        pattern_identity = r"^\d{12}$"
        if not re.match(pattern_identity, self.gov_identity):
            raise ValidationError("Invalid Gov. Identity number. Please enter a 12-digit number.")

        # Validate email
        pattern_email = r'^[a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,4}$'
        if not re.match(pattern_email, self.email):
            raise ValidationError("Invalid email. Please enter a correct email address.")

    @api.depends("date_of_birth")
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                age = relativedelta(date.today(), rec.date_of_birth)
                if age.years > 0:
                    rec.patient_age = f"{age.years} Years"
                elif age.months > 0:
                    rec.patient_age = f"{age.months} Months"
                else:
                    rec.patient_age = f"{age.days} Days"
            else:
                rec.patient_age = "0"

    @api.model
    def create(self,vals):
        # pdb.set_trace()
        vals['name']=vals.get("patient_name")
        vals['login']=vals.get("email")
        decoded_image=vals.get("image")
        vals['image']=base64.b64decode(decoded_image).decode()
        return super(hospital_patient, self).create(vals)

    def action_get_treatment_record(self):
        # This will make sure we have one record, not multiple records.
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Treatment',
            'view_mode': 'tree',
            'res_model': 'hospital.treatment',
            'domain': [('patient_id', '=', self.patient_name)],
            'context': "{'create': False}"
        } 

class ResPartner(models.Model):
    _inherit = "res.partner"
    treatment_count = fields.Integer(string="Treatment",compute='compute_treatment_count',default=0)
    
    def compute_treatment_count(self):
        for record in self:
            record.treatment_count = self.env['hospital.treatment'].search_count(
                [('patient_id', '=', self.name)]) 