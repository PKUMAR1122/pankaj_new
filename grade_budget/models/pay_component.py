from odoo import api, fields, models

class PayComponent(models.Model):
    _name = 'pay.component'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Pay Component'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    name_arabic = fields.Char(string='Name in Arabic ')
    account_id = fields.Many2one('account.account', string='Budget Account')
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], string='Status', default='active')
