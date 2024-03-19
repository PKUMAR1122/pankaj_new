from odoo import api, fields, models

class Grade(models.Model):
    _name = 'grade'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Grade'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    name_arabic = fields.Char(string='Name in Arabic ')
    # approve_count = fields.Integer(string='Approve Count')
