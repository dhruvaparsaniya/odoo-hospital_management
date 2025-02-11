from odoo import api, fields, models
from odoo.exceptions import ValidationError


class hospital_treatment(models.Model):
    _name = "hospital.treatment"
    _description = "Treatment"
    _rec_name = "treatment_id"

    treatment_id = fields.Char("Treatment ID", default="id", readonly=True)
    diagnosis = fields.One2many("hospital.diagnosis", "treatment_id", string="Diagnosis")
    patient_id = fields.Many2one("hospital.patient", string="Patient Name", required=True)
    physician_id = fields.Many2one("hospital.physician", string="Physician Name", required=True)
    treatment_date = fields.Date("Treatment Date", required=True)
    state = fields.Selection(
        [("draft", "Draft"), ("confirm", "Confirm"), ("done", "Done"), ("cancel", "Cancel")],
        default="draft",
    )
    sales_count = fields.Integer(string="Sales", compute='compute_sales_count', default=0)

    @api.constrains("treatment_date")
    def validate_constrains(self):
        current_date = fields.Date.today()
        if self.treatment_date and self.treatment_date < current_date:
            raise ValidationError("Invalid treatment date. Please select a future or current date.")

    @api.model
    def create(self, vals):
        vals["treatment_id"] = (
            self.env["ir.sequence"].sudo().next_by_code("hospital.record") or "New"
        )
        return super(hospital_treatment, self).create(vals)

    def action_send_mail(self, mail_type):
        template = self.env.ref(mail_type)
        template.send_mail(self.id, force_send=True)

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    def action_activate(self):
        for rec in self:
            rec.state = "confirm"
        self.action_send_mail('Hospital1.confirm_email_template')

    def action_done(self):
        for rec in self:
            rec.state = "done"
        self.action_send_mail('Hospital1.done_email_template')

    def action_cancel(self):
        for rec in self:
            rec.state = "cancel"
        self.action_send_mail('Hospital1.cancle_email_template')

    def action_open_product_wizard(self):
        return {
            "name": "Product Wizard",
            "type": "ir.actions.act_window",
            "res_model": "product.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_treatment_id": self.id},
        }
    
    def action_get_sales_record(self):
        # This will make sure we have one record, not multiple records.
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales',
            'view_mode': 'tree',
            'res_model': 'sale.order',
            'domain': [('treatment_id', '=', self.treatment_id)],
            'context': "{'create': False}"
        }
    
    def compute_sales_count(self):
        for record in self:
            record.sales_count = self.env['sale.order'].search_count(
                [('treatment_id', '=', self.treatment_id)])

    def action_print_custom_report(self):
        return self.env.ref("Hospital1.action_report_treatment").report_action(self)
