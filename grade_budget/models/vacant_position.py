from odoo import api, fields, models, _
from odoo.exceptions import UserError

class VacantPostion(models.Model):
    _name = 'vacant.position'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Vacant Position'
    _rec_name = 'grade'

    grade = fields.Many2one('grade', string='Grade')
    vacant_number = fields.Integer('Vacant Position', compute='_compute_vacant_position')
    vacant_position_line = fields.One2many('vacant.position.lines', 'vacant_position_id', string='Vacant Position Lines')
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
    
    @api.depends('grade','category_id', 'job_id', 'budget_id')
    def _compute_vacant_position(self):
        for val in self:
            if val.grade and val.category_id and val.budget_id:
                job_id = val.job_id and val.job_id.id or False
                grade_category_job = self.env['grade.category.job.mapping'].search([('budget_id', '=', val.budget_id.id),
                                                                                    ('grade', '=', val.grade.id),
                                                                                    ('category', '=', val.category_id.id),
                                                                                    ('job_id', '=', job_id)],limit=1)
                employee_ids = self.env['hr.employee'].search([('grade', '=', val.grade.id),
                                                               ('category_id', '=', val.category_id.id),
                                                               ('grade_job_id', '=', job_id),
                                                               ('budget_id', '=', val.budget_id.id),
                                                               ('active', '=', True)])
                
                if employee_ids and grade_category_job:
                    val.vacant_number = grade_category_job.approve_count - len(employee_ids.ids)
                elif grade_category_job:
                    val.vacant_number = grade_category_job.approve_count
                else:
                    val.vacant_number = 0 
            else:
                val.vacant_number = 0        
                
    @api.onchange('fy_id')
    def _onchange_fy_id(self):
        if self.fy_id:
            self.date_from = self.fy_id.date_from
            self.date_to = self.fy_id.date_to

    @api.depends('vacant_position_line','vacant_position_line.amount')
    def _compute_total_amount(self):
        for vacant in self:
            vacant.total_amount = sum(vacant.vacant_position_line.mapped('amount'))

    def load_vacant_pay_components(self):
        if self.grade and self.category_id and self.budget_id:
            job_id = self.job_id and self.job_id.id or False
            grade_category_job = self.env['grade.category.job.mapping'].search([
                                                                                ('grade', '=', self.grade.id),
                                                                                ('category', '=', self.category_id.id),
                                                                                ('job_id', '=', job_id),
                                                                                ('budget_id', '=', self.budget_id.id),
                                                                                ])
            new_lines = []
            if self.vacant_position_line:
                self.vacant_position_line.unlink()
            for grade_line in grade_category_job:
                for count in range(self.vacant_number):
                    for rec in grade_line.grade_category_lines:
                        new_line = (0, 0, {
                            'amount': rec.amount,
                            'pay_component_id': rec.pay_component_id.id,
                        })
                        new_lines.append(new_line)
            self.vacant_position_line = new_lines


class VacantPositionLines(models.Model):
    _name = 'vacant.position.lines'

    vacant_position_id = fields.Many2one('vacant.position')
    pay_component_id = fields.Many2one('pay.component', string='Pay Component')
    project_id = fields.Many2one('project.project', string='Program')
    activity_id = fields.Many2one('project.task', string='Activity')
    sub_activity_id = fields.Many2one('project.task', string='Sub Activity')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
