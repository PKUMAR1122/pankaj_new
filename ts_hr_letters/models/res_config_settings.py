from odoo import api, fields, models, _
import base64


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)
    external_letter_layout_id = fields.Many2one(related="company_id.external_letter_layout_id", readonly=False,
                                                string="External Letter Layout")

    def edit_custom_external_header(self):
        if not self.external_letter_layout_id:
            return False

        return {
            'name': 'External Letter Layout View',
            'type': 'ir.actions.act_window',
            'res_model': 'ir.ui.view',
            'view_mode': 'form',
            'res_id': self.external_letter_layout_id.id,
        }

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(external_letter_layout_id=int(self.env['ir.config_parameter'].sudo().get_param('ts_hr_letters.external_letter_layout_id', False)),)
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('ts_hr_letters.external_letter_layout_id', self.external_letter_layout_id.id or False)


class ResCompany(models.Model):
    _inherit = "res.company"

    external_letter_layout_id = fields.Many2one('ir.ui.view', 'Letters Template')