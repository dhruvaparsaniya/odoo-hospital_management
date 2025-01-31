from odoo import fields, models

class custom_sale_order(models.Model):

    _inherit='sale.order'

    treatment_id=fields.Many2one("hospital.treatment","Treatment_id",readonly=True)