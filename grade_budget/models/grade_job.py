from odoo import api, fields, models


class GradeJob(models.Model):
    _name = 'grade.job'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Grade'
    _rec_name = 'job_name'

    job_name = fields.Char(string='Job Name')
    name_arabic = fields.Char(string='Job Name in Arabic ')
    category_id = fields.Many2one('grade.category',string="Category")
    status = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string='Status', default='confirm')






