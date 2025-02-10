import base64
from odoo import models, api, fields
import io
import xlsxwriter


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_generate_xlsx_report(self):
        invoices = self.env['account.move'].search([('move_type', '=', 'out_invoice')])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Invoices")
        bold = workbook.add_format({'bold': True})

        headers = ['Invoice Number', 'Customer', 'Product', 'Quantity', 'Unit Price', 'Date', 'Total Amount']
        for col, header in enumerate(headers):
            sheet.write(0, col, header, bold)

        row = 1
        for invoice in invoices:
            first_line = True
            for line in invoice.invoice_line_ids:
                if first_line:
                    sheet.write(row, 0, invoice.name)
                    sheet.write(row, 1, invoice.partner_id.name)
                    sheet.write(row, 5, str(invoice.invoice_date))
                    sheet.write(row, 6, invoice.amount_total)
                    first_line = False
                else:
                    sheet.write(row, 0, "")
                    sheet.write(row, 1, "")
                    sheet.write(row, 5, "")
                    sheet.write(row, 6, "")

                # Add product details for each line
                sheet.write(row, 2, line.product_id.name)
                sheet.write(row, 3, line.quantity)
                sheet.write(row, 4, line.price_unit)
                row += 1

        workbook.close()
        output.seek(0)
        datas = base64.b64encode(output.read())

        attachment = self.env['ir.attachment'].create({
            'name': 'Invoices Report.xlsx',
            'datas': datas,
            'res_model': self._name,
            'res_id': self.id,
            'type': 'binary',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'new',
        }
