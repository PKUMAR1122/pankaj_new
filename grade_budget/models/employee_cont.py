from odoo import fields, models, api

class EmployeeContract(models.Model):
    _name = 'employee.contract'
    _description = 'Employee Contract'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee',string='Employee')
    department_id = fields.Many2one('hr.department',string='Department')
    contract_start_date = fields.Date(string='Contract Start Date')
    contract_end_date = fields.Date(string='Contract End Date')
    position_id = fields.Many2one('hr.job',string='Position')
    activity_id = fields.Many2one('project.task', string='Activity')
    sub_activity_id = fields.Many2one('project.task',string='Sub Activity')
    project_id = fields.Many2one('project.project',string='Program')
    grade_details_id = fields.Many2one('grade',string='Grade')
    category_id = fields.Many2one('grade.category', string='Category Id')
    grade_job_id = fields.Many2one('grade.job', string='Job')
    employee_cont_line_ids = fields.One2many('employee.contract.lines', 'employee_cont_id', string='Employee Line')
    total_amount = fields.Monetary(string='Total Amount', compute='_compute_total_amount', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    budget_id = fields.Many2one(comodel_name='master.budget', string='Budget Number')
    is_unified = fields.Boolean(related='category_id.is_unified', string="Unified")
    
    @api.depends('employee_cont_line_ids', 'employee_cont_line_ids.amount')
    def _compute_total_amount(self):
        for val in self:
            val.total_amount = sum(val.employee_cont_line_ids.mapped('amount'))

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.department_id = self.employee_id.department_id.id
        self.position_id = self.employee_id.job_id
        self.project_id = self.employee_id.project_id
        self.activity_id = self.employee_id.activity_id
        self.sub_activity_id = self.employee_id.sub_activity_id
        self.grade_details_id = self.employee_id.grade
        self.category_id = self.employee_id.category_id
        self.grade_job_id = self.employee_id.grade_job_id
        self.budget_id = self.employee_id.budget_id

    @api.onchange('grade_details_id', 'category_id', 'grade_job_id', 'budget_id')
    def _onchange_grade_category_job(self):
        if self.grade_details_id and self.category_id and self.budget_id:
            grade_job_id = self.grade_job_id and self.grade_job_id.id or False
            grade_category_job = self.env['grade.category.job.mapping'].search([
                ('grade', '=', self.grade_details_id.id),
                ('category', '=', self.category_id.id),
                ('job_id', '=', grade_job_id),
                ('budget_id', '=', self.budget_id.id)
            ])
            self.employee_cont_line_ids = [(5, 0, 0)]
            new_lines = []
            for grade_line in grade_category_job:
                for rec in grade_line.grade_category_lines:
                    new_line = (0, 0, {
                        'amount': rec.amount,
                        'pay_component_id': rec.pay_component_id.id,
                    })
                    new_lines.append(new_line)
            self.employee_cont_line_ids = new_lines


class EmployeeContractLine(models.Model):
    _name = 'employee.contract.lines'
    _description = 'Employee Contract Line'

    employee_cont_id = fields.Many2one('employee.contract')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    pay_component_id = fields.Many2one('pay.component',string='Budget Account Component')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)


