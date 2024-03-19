from odoo import fields, models, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    name_arabic = fields.Char(string='Name in Arabic ')
    civil_service_no = fields.Char(string='Civil Service Number')
    emp_no = fields.Char(string='Employee Number')
    manpower_no = fields.Char(string='Manpower Number')
    doj = fields.Date(string='Date of Joining')
    # dob = fields.Date(string='Date of Birth')
    # passport_no = fields.Char(string='Passport Number')
    civil_id_no = fields.Char(string='Civil ID Number')
    grade = fields.Many2one('grade', string='Grade')
    date_of_occupation = fields.Date(string='Date of Occupation')
    status = fields.Selection([('job_title_change','Job title change'),('change_of_name','Change of name'),
                               ('duplication_services','Duplication Services'),
                               ('developments','Developments')],string='Change Reason')
    qualification = fields.Char(string='Qualfication')
    specialization = fields.Char(string='Specialization')
    educational_institution = fields.Char(string='Educational Institution')
    graduation_country = fields.Many2one('res.country', string='Graduation Country')
    date_of_qualification = fields.Date(string='Date of Qualification')
    job = fields.Char(string='Job Id')
    # position = fields.Char(string='Position')
    section = fields.Many2one('master.section',string='Section')
    # department = fields.Char(string='Department')
    directorate = fields.Char(string='Directorate')
    sector = fields.Char(string='Sector')
    government_entity = fields.Char(string='Government Entity')
    # budjet = fields.Integer(string='Budjet Number')
    budjet_name = fields.Char(string='Budget Name')
    leave_credit = fields.Float(string='Leave Credit')
    basic_salary = fields.Float(string='Basic Salary')
    transfer_allow = fields.Float(string='Transfer Allowance')
    accommodation = fields.Float(string='Accommodation')
    electricity = fields.Float(string='Electricity')
    water = fields.Float(string='Water')
    cost_of_living_allow = fields.Float(string='Cost of Living Allowance')
    work_nature_allow = fields.Float(string='Work Nature Allowance')
    other_allow = fields.Float(string='Other Allowance')
    retirement_fund_deduction = fields.Float(string='Retirement Fund Deduction')
    other_deduction = fields.Float(string='Other Deduction')
    total = fields.Float(string='Total')
    bank_name = fields.Char(string='Bank Name')
    bank_code = fields.Char(string='Bank Code')
    branch = fields.Char(string='Branch')
    branch_code = fields.Char(string='Branch Code')
    # account_number = fields.Integer(string='Account Number')
    activity_id = fields.Many2one('project.task', string='Activity')
    sub_activity_id = fields.Many2one('project.task', string='Sub Activity')
    project_id = fields.Many2one('project.project', string='Program')
    category_id = fields.Many2one('grade.category', string='Category Id')
    grade_job_id = fields.Many2one('grade.job', string='Job')
    # budget_id = fields.Many2one(comodel_name='crossovered.budget', string='Budget Number')
    budget_id = fields.Many2one(comodel_name='master.budget', string='Budget Number')
    is_unified = fields.Boolean(related='category_id.is_unified', string="Unified")
    
    @api.onchange('project_id')
    def onchange_program_id(self):
        self.activity_id = False
        self.sub_activity_id = False
    
    @api.onchange('activity_id')
    def onchange_activity_id(self):
        self.sub_activity_id = False

