# from . import convert_number_to_word
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.osv.expression import AND

# class GradeBudgetFinal(models.Model):
#     _name = 'final.grade.budget'

#     name = fields.Char("Done")
    # access_final_grade_budget,final.grade.budget,model_final_grade_budget,base.group_user,1,1,1,1


class GradeBudgetEstimation(models.Model):
    _inherit = 'final.budget.estimation'
    
    budget_id = fields.Many2one(comodel_name='master.budget', string='Budget Number')
    grade = fields.Many2one('grade', string='Grade')
    category_id = fields.Many2one('grade.category', string='Category Id')
    job_id = fields.Many2one('grade.job', string='Job')
    is_unified = fields.Boolean(related='category_id.is_unified', string="Unified")

    def grade_load_lines(self):
        if self.final_budget_estimation_line:
            self.final_budget_estimation_line.unlink()
        if self.account_base_budget_lines:
            self.account_base_budget_lines.unlink()
        if self.performance_budget_lines:
            self.performance_budget_lines.unlink()
        if self.activity_sub_activity_base_budget_lines:
            self.activity_sub_activity_base_budget_lines.unlink()
            
        job_id = self.job_id and self.job_id.id or False

        domain = [('date_to', '<=', self.date_to),('date_from', '>=', self.date_from),('state', '=', 'confirm'),
                  ('budget_id', '=', self.budget_id.id),('grade', '=', self.grade.id),
                  ('category_id', '=', self.category_id.id),('job_id', '=', job_id)]
        
        contract_domain = [('employee_id.active', '=', True),
                           ('budget_id', '=', self.budget_id.id),('grade_details_id', '=', self.grade.id),
                           ('category_id', '=', self.category_id.id),('grade_job_id', '=', job_id)]
        
        vacant_position_ids = self.env['vacant.position'].search(domain)
        new_position_ids = self.env['new.position'].search(domain)
        contract_ids = self.env['employee.contract'].search(contract_domain)
        final_lines_dict = {}

        for rec in vacant_position_ids:
            for line in rec.vacant_position_line:
                department_id = False
                account_id = line.pay_component_id.account_id.id
                planned_amount = line.amount
                project_id = line.project_id.id if line.project_id else False
                activity_id = line.activity_id.id if line.activity_id else False
                sub_activity_id = line.sub_activity_id.id if line.sub_activity_id else False
                if line.sub_activity_id:
                    department_id = line.sub_activity_id.department_id.id
                elif line.activity_id:
                    department_id = line.activity_id.department_id and line.activity_id.department_id.id or False
                
                line_key = (department_id, account_id, project_id, activity_id, sub_activity_id)
                
                if line_key in final_lines_dict:
                    final_lines_dict[line_key] += planned_amount
                else:
                    final_lines_dict[line_key] = planned_amount
                    
        for rec in new_position_ids:
            for line in rec.new_position_line:
                department_id = False
                account_id = line.pay_component_id.account_id.id
                planned_amount = line.amount
                project_id = line.project_id.id if line.project_id else False
                activity_id = line.activity_id.id if line.activity_id else False
                sub_activity_id = line.sub_activity_id.id if line.sub_activity_id else False
                if line.sub_activity_id:
                    department_id = line.sub_activity_id.department_id.id
                elif line.activity_id:
                    department_id = line.activity_id.department_id and line.activity_id.department_id.id or False
                
                line_key = (department_id, account_id, project_id, activity_id, sub_activity_id)
                
                if line_key in final_lines_dict:
                    final_lines_dict[line_key] += planned_amount
                else:
                    final_lines_dict[line_key] = planned_amount
                    
        for rec in contract_ids:
            department_id = rec.department_id.id
            project_id = rec.project_id.id if rec.project_id else False
            activity_id = rec.activity_id.id if rec.activity_id else False
            sub_activity_id = rec.sub_activity_id.id if rec.sub_activity_id else False
            for line in rec.employee_cont_line_ids:
                account_id = line.pay_component_id.account_id.id
                planned_amount = line.amount
                
                line_key = (department_id, account_id, project_id, activity_id, sub_activity_id)
                if line_key in final_lines_dict:
                    final_lines_dict[line_key] += planned_amount
                else:
                    final_lines_dict[line_key] = planned_amount
                    
        for line_key, planned_amount in final_lines_dict.items():
            department_id, account_id, project_id, activity_id, sub_activity_id = line_key
    
            self.env['final.budget.estimation.lines'].create({
                'final_budget_estimation_id': self.id,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'account_id': account_id,
                'grade_planned_amount': planned_amount,
                'project_id': project_id,
                'activity_id': activity_id,
                'sub_activity_id': sub_activity_id,
                'department_id':department_id,
            })
            