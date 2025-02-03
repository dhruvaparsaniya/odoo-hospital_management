from odoo import api, fields, models

class hospital_physician_speciality(models.Model):
    _name = "hospital.speciality"
    _description = "Physician Speciality"
    
    physician_speciality_id = fields.Char(string="Speciality ID", default='new', readonly=False)
    name = fields.Char(string="Speciality Name", required=True)
    
    @api.model
    def create(self, vals):
        vals['physician_speciality_id'] = self.env['ir.sequence'].sudo().next_by_code("physician.speciality") or 'New'
        res = super(hospital_physician_speciality,self).create(vals)
        return res