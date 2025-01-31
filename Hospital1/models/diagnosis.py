from datetime import date
from odoo import api, fields, models

class hospital_diagnosis(models.Model):
    _name="hospital.diagnosis"
    _description="diagnosis data"

    diseases= fields.Many2one('hospital.diseases','Diseases')
    treatment_id=fields.Many2one('hospital.treatment')
    type= fields.Selection([('high','High'),('medium','Medium'),('low','Low')])
    date=fields.Date('Date',required=True,readonly=True, default=lambda *a: date.today() )
    # current_user = fields.Many2one('res.users','Current User', default=lambda self: self.env.user,readonly=True)