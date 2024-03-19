from odoo import api, fields, models, _
from odoo.exceptions import UserError



class NewPosition(models.Model):
    _name = 'new.position'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'New Position'
    _rec_name = 'grade'

    grade = fields.Many2one('grade', string='Grade')
    count = fields.Integer(string='New Position')
    department_id = fields.Many2one('hr.department', string='Department')
    section = fields.Many2one('master.section', string='Section')
    new_position_line = fields.One2many('new.position.lines', 'new_position_id', string='New Position Lines')
    total_amount = fields.Monetary(string='Total Amount', compute='_compute_total_amount', currency_field='currency_id')
    fy_id = fields.Many2one('account.fiscal.year', string='Fiscal Year')
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    category_id = fields.Many2one('grade.category', string='Category Id')
    job_id = fields.Many2one('grade.job', string='Job')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('cancel', 'Cancelled')], 
                             'Status', default='draft', index=True, readonly=True, copy=False, tracking=True)
    budget_id = fields.Many2one(comodel_name='master.budget', string='Budget Number')
    is_unified = fields.Boolean(related='category_id.is_unified', string="Unified")
    
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            
    def action_cancel(self):
        for rec in self:
            if rec.state == 'confirm':
                raise UserError(_('This record already approved. Refresh your browser.!'))
            rec.state = 'cancel'
            
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.onchange('fy_id')
    def _onchange_fy_id(self):
        if self.fy_id:
            self.date_from = self.fy_id.date_from
            self.date_to = self.fy_id.date_to

    @api.depends('new_position_line','new_position_line.amount')
    def _compute_total_amount(self):
        for new in self:
            new.total_amount = sum(new.new_position_line.mapped('amount'))

    def load_new_pay_components(self):
        if self.grade and self.category_id and self.budget_id:
            job_id = self.job_id and self.job_id.id or False
            grade_category_job = self.env['grade.category.job.mapping'].search([('budget_id', '=', self.budget_id.id),
                                                                                ('grade', '=', self.grade.id),
                                                                                ('category', '=', self.category_id.id),
                                                                                ('job_id', '=', job_id)])
            if self.new_position_line:
                self.new_position_line.unlink()
            new_lines = []
            for grade_line in grade_category_job:
                for count in range(self.count):
                    for rec in grade_line.grade_category_lines:
                        new_line = (0, 0, {
                            'amount': rec.amount,
                            'pay_component_id': rec.pay_component_id.id,
                        })
                        new_lines.append(new_line)
            self.new_position_line = new_lines

class NewPositionLines(models.Model):
    _name = 'new.position.lines'

    new_position_id = fields.Many2one('new.position')
    pay_component_id = fields.Many2one('pay.component', string='Pay Component')
    project_id = fields.Many2one('project.project', string='Program')
    activity_id = fields.Many2one('project.task', string='Activity')
    sub_activity_id = fields.Many2one('project.task', string='Sub Activity')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
