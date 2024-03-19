from odoo import api, fields, models


class GradeCategoryJob(models.Model):
    _name = 'grade.category.job.mapping'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Grade'
    _rec_name = 'grade'

    grade = fields.Many2one('grade',string='Grade')
    category = fields.Many2one('grade.category',string='Category')
    job_id = fields.Many2one('grade.job',string="Job")
    grade_category_lines = fields.One2many('grade.category.job.lines', 'grade_cat_job_id', string='Grade Category Lines')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    total_amount = fields.Monetary(string='Total Amount', compute='_compute_total_amount', currency_field='currency_id')
    approve_count = fields.Integer(string='Approve Count')
    budget_id = fields.Many2one(comodel_name='master.budget', string='Budget Number')
    is_unified = fields.Boolean(related='category.is_unified', string="Unified")

    @api.depends('grade_category_lines', 'grade_category_lines.amount')
    def _compute_total_amount(self):
        for grade in self:
            grade.total_amount = sum(grade.grade_category_lines.mapped('amount'))

class Grade(models.Model):
    _name = 'grade.category.job.lines'

    grade_cat_job_id = fields.Many2one('grade.category.job.mapping')
    pay_component_id = fields.Many2one('pay.component', string='Budget Account Component ID')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)







