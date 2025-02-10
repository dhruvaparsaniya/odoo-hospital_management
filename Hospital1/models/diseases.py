from odoo import fields, models


class hospital_dieases(models.Model):
    _name = "hospital.diseases"
    _description = "diseases data"
    _rec_name = 'diseases_name'

    diseases_name = fields.Char("diseases name", required=True)
    code = fields.Char("diseases code", required=True)
