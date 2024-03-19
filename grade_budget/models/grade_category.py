from odoo import api, fields, models


class GradeCategory(models.Model):
    _name = 'grade.category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Grade'

    name = fields.Char(string=' Category Name')
    name_arabic = fields.Char(string='Name in Arabic ')
    status = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string='Status', default='confirm')
    is_unified = fields.Boolean(string="Unified", default=False)






