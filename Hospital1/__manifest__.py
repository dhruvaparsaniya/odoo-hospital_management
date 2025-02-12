{
    "name": "Hospital Management",
    "author": "Dhruva",
    "license": "LGPL-3",
    "data": [
        'security/security.xml',
        "security/ir.model.access.csv",

        "report/treatment_report_template.xml",
        "report/report.xml",

        "data/ir_action_data.xml",
        "data/ir_cron_data.xml",
        "data/email_template.xml",
        "data/sequence_hospital.xml",

        "views/custom_invoice_view.xml",
        "views/register_template.xml",
        "views/custom_sale_view.xml",
        "views/physician_speciality_view.xml",
        "views/diagnosis_view.xml",
        "views/diseases_view.xml",
        "views/treatment_view.xml",
        "views/patient_view.xml",
        "views/physician_view.xml",
        "views/menu.xml",

        "wizard/product_wizard_view.xml",
    ],
    "depends": [
        "sale",
        "web",
        "mail"
    ],
}
