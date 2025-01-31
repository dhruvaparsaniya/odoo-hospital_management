from odoo import models, fields, api
from odoo.exceptions import UserError

class hospital_treatment_wizard(models.TransientModel):
    _name = "product.wizard"
    _description = "product wizard"

    treatment_ids = fields.Many2one(
        "hospital.treatment",
        string="Treatment",
        required=True,
        default=lambda self: self.env.context.get("default_treatment_id") or False,
        readonly=True
    )

    product_ids = fields.Many2many("product.product", string="Products", required=True)

    def confirm_action(self):
        sale_order = self.create_sale_order()
        return {
            "name": "Sale Order",
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "view_mode": "form",
            "res_id": sale_order.id,
            "target": "current",
        }

    def create_sale_order(self):
        if not self.product_ids:
            raise UserError(
                "Please select at least one product to create a sale order."
            )

        partner_id = self.treatment_ids.patient_id.partner_id.id

        order_lines = [
            (0, 0, {"product_id": product.id, "product_uom_qty": 1 })
            for product in self.product_ids
        ]

        sale_order = self.env["sale.order"].create(
            {
                "partner_id": partner_id,
                "order_line": order_lines,
            }
        )
        return sale_order