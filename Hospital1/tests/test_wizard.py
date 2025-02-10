from odoo.tests.common import TransactionCase
from datetime import date


class TestWizard(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestWizard, cls).setUpClass()
        # import pdb;pdb.set_trace()
        cls.treatment = cls.env['hospital.treatment'].create({
            'patient_id': 1,
            'physician_id': 2,
            'treatment_date': date(2025, 2, 12),
            'sales_count': 2,
        })
        cls.product_1 = cls.env['product.product'].create({'name': 'Product 1'})

    def test_wizard_creation(self):
        wizard = self.env['product.wizard'].create({
            'treatment_ids': self.treatment.id,
            'product_ids': [(6, 0, [self.product_1.id])],
        })
        self.assertEqual(wizard.treatment_ids, self.treatment, "wizard not created")

    def test_creates_sale_order(self):
        partner_id = self.treatment.patient_id.id
        order_lines = [
            (0, 0, {"product_id": self.product_1.id, "product_uom_qty": 1})
        ]
        order = self.env['sale.order'].create({
            "partner_id": partner_id,
            "order_line": order_lines,
        })

        self.assertEqual(order.partner_id.id, partner_id, "invalid partner id")
        self.assertEqual(len(order.order_line), 1, "Invalid product count")

    def test_invalid_creates_sale_order(self):
        partner_id = self.treatment.patient_id.id
        order_lines = [
            (0, 0, {"product_id": self.product_1.id, "product_uom_qty": 1})
        ]
        order = self.env['sale.order'].create({
            "partner_id": partner_id,
            "order_line": order_lines,
        })
        self.assertEqual(order.partner_id.id, 2, "Invalid partner id")
        self.assertEqual(len(order.order_line), 2, "Invalid product count")
