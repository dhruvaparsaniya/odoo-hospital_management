from odoo.tests.common import TransactionCase
from datetime import date


class TestHospitalPatient(TransactionCase):

    @classmethod
    def setUpClass(self):
        super(TestHospitalPatient, self).setUpClass()
        self.patient = self.env['hospital.patient'].sudo().create({
            'patient_name': 'Patient One',
            'email': 'test1@example.com',
            'date_of_birth': date(1990, 1, 1),
            'mobile_number': '1234567890',
            'gov_identity': '111111111111',
            'gender': 'male',
        })

    def test_email_validation(self):
        valid_email = "test1@example.com"
        self.assertEqual(self.patient.email, valid_email, "InValid email should be accepted.")

    def test_invalid_email_validation(self):
        invalid_email = "test1.com"
        self.assertEqual(self.patient.email, invalid_email, "InValid email should be accepted.")

    def test_compute_age(self):
        valid_age = '35 Years'
        self.assertEqual(self.patient.patient_age, valid_age, 'InValid age calculation')

    def test_invalid_compute_age(self):
        invalid_age = '32 Years'
        self.assertEqual(self.patient.patient_age, invalid_age, 'InValid age calculation')

    def test_future_date_of_birth_validation(self):
        current_date = date(2025, 2, 4)
        self.assertTrue(self.patient.date_of_birth >= current_date, msg="Invalid input,future dates as birthdate")
