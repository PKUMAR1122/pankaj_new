from odoo import api, fields, models, _
import base64
from odoo.exceptions import UserError


class HREmployee(models.Model):
    _inherit = "hr.employee"

    ts_resignation_date = fields.Date(string="Resignation Date")






    def action_appraisal_letter(self):
        template_id = self.env.ref('ts_hr_letters.email_template_appraisal_letter').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        template = self.env['mail.template'].browse(template_id)

        appraisal_report = self.env.ref('ts_hr_letters.action_appraisal_letter_report')
        data_record = base64.b64encode(self.env['ir.actions.report'].sudo()._render_qweb_pdf(appraisal_report, [self.id], data=None)[0])
        ir_values = {
            'name': 'Appraisal Letter',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
            'res_model': 'hr.applicant',
        }
        appraisal_report_attachment_id = self.env['ir.attachment'].sudo().create(ir_values)
        ctx = {
            'default_model': 'hr.employee',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': False,
            'default_attachment_ids': [(4, appraisal_report_attachment_id.id)]
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_experience_letter(self):
        lst = ['ts_resignation_date', 'company_id', 'job_id']
        missing_fields = []
        for field_name in lst:
            if not getattr(self, field_name, False):
                field_string = self._fields[field_name].string
                missing_fields.append(field_string)
        if missing_fields:
            fields_string = ', '.join(missing_fields)
            raise UserError(_('Missing required fields: %s') % fields_string)

        template_id = self.env.ref('ts_hr_letters.email_template_experience_letter').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        template = self.env['mail.template'].browse(template_id)
        experience_report = self.env.ref('ts_hr_letters.action_experience_letter_report')
        data_record = base64.b64encode(self.env['ir.actions.report'].sudo()._render_qweb_pdf(experience_report, [self.id], data=None)[0])
        ir_values = {
            'name': 'Relieving Cum Experience Letter',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
            'res_model': 'hr.applicant',
        }
        experience_report_attachment_id = self.env['ir.attachment'].sudo().create(ir_values)
        ctx = {
            'default_model': 'hr.employee',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': False,
            'default_attachment_ids': [(4, experience_report_attachment_id.id)]
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_resignation_letter(self):
        lst = ['ts_resignation_date', 'company_id', 'parent_id']
        missing_fields = []
        for field_name in lst:
            if not getattr(self, field_name, False):
                field_string = self._fields[field_name].string
                missing_fields.append(field_string)
        if missing_fields:
            fields_string = ', '.join(missing_fields)
            raise UserError(_('Missing required fields: %s') % fields_string)

        template_id = self.env.ref('ts_hr_letters.email_template_resignation_letter').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        template = self.env['mail.template'].browse(template_id)

        resignation_report = self.env.ref('ts_hr_letters.action_resignation_letter_report')
        data_record = base64.b64encode(self.env['ir.actions.report'].sudo()._render_qweb_pdf(resignation_report, [self.id], data=None)[0])
        ir_values = {
            'name': 'Resignation Acceptance Letter',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
            'res_model': 'hr.applicant',
        }
        resignation_report_attachment_id = self.env['ir.attachment'].sudo().create(ir_values)
        ctx = {
            'default_model': 'hr.employee',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': False,
            'default_attachment_ids': [(4, resignation_report_attachment_id.id)]
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_appointment_letter(self):
        lst = ['company_id']
        missing_fields = []
        for field_name in lst:
            if not getattr(self, field_name, False):
                field_string = self._fields[field_name].string
                missing_fields.append(field_string)
        if missing_fields:
            fields_string = ', '.join(missing_fields)
            raise UserError(_('Missing required fields: %s') % fields_string)

        template_id = self.env.ref('ts_hr_letters.email_template_appointment_letter').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        template = self.env['mail.template'].browse(template_id)

        # Render the appointment letter report and create an attachment
        appointment_report = self.env.ref('ts_hr_letters.action_appointment_letter_report')
        data_record = base64.b64encode(self.env['ir.actions.report'].sudo()._render_qweb_pdf(appointment_report, [self.id], data=None)[0])
        ir_values = {
            'name': 'Appointment Letter',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
            'res_model': 'hr.applicant',
        }
        appointment_report_attachment = self.env['ir.attachment'].sudo().create(ir_values)

        # Compose the email using the mail template
        ctx = {
            'default_model': 'hr.employee',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': False,
            'default_attachment_ids': [(4, appointment_report_attachment.id)]
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_promotion_letter(self):
        template_id = self.env.ref('ts_hr_letters.email_template_promotion_letter').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        template = self.env['mail.template'].browse(template_id)
        ctx = {
            'default_model': 'hr.employee',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': False,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


class HRApplicant(models.Model):
    _inherit = "hr.applicant"

    def action_offer_letter(self):
        lst = ['company_id', 'partner_name', 'job_id']
        missing_fields = []
        for field_name in lst:
            if not getattr(self, field_name, False):
                field_string = self._fields[field_name].string
                missing_fields.append(field_string)
        if missing_fields:
            fields_string = ', '.join(missing_fields)
            raise UserError(_('Missing required fields: %s') % fields_string)

        template_id = self.env.ref('ts_hr_letters.email_template_offer_letter').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        template = self.env['mail.template'].browse(template_id)
        offer_letter_rpt_id = self.env.ref('ts_hr_letters.action_offer_letter_report')
        data_record = base64.b64encode(self.env['ir.actions.report'].sudo()._render_qweb_pdf(offer_letter_rpt_id, [self.id], data=None)[0])
        ir_values = {
            'name': 'Offer Letter',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
            'res_model': 'hr.applicant',
        }
        offer_letter_rpt_attachment_id = self.env['ir.attachment'].sudo().create(ir_values)
        ctx = {
            'default_model': 'hr.applicant',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': False,
            'default_attachment_ids': [(4, offer_letter_rpt_attachment_id.id)]
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_erp_creation(self):
        lst = ['partner_name', 'email_from', 'job_id', 'department_id']
        missing_fields = []
        for field_name in lst:
            if not getattr(self, field_name, False):
                field_string = self._fields[field_name].string
                missing_fields.append(field_string)
        if missing_fields:
            fields_string = ', '.join(missing_fields)
            raise UserError(_('Missing required fields: %s') % fields_string)

        template_id = self.env.ref('ts_hr_letters.email_template_erp_creation').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        template = self.env['mail.template'].browse(template_id)
        ctx = {
            'default_model': 'hr.employee',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': False,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_mail_id_creation(self):
        lst = ['partner_name', 'availability', 'email_from', 'job_id']
        missing_fields = []
        for field_name in lst:
            if not getattr(self, field_name, False):
                field_string = self._fields[field_name].string
                missing_fields.append(field_string)
        if missing_fields:
            fields_string = ', '.join(missing_fields)
            raise UserError(_('Missing required fields: %s') % fields_string)

        template_id = self.env.ref('ts_hr_letters.email_template_mail_creation_id').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        template = self.env['mail.template'].browse(template_id)
        ctx = {
            'default_model': 'hr.applicant',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': False,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_send_email_joining(self):
        lst = ['company_id', 'partner_name']
        missing_fields = []
        for field_name in lst:
            if not getattr(self, field_name, False):
                field_string = self._fields[field_name].string
                missing_fields.append(field_string)
        if missing_fields:
            fields_string = ', '.join(missing_fields)
            raise UserError(_('Missing required fields: %s') % fields_string)

        template_id = self.env.ref('ts_hr_letters.email_template_joining_letter').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        template = self.env['mail.template'].browse(template_id)
        ctx = {
            'default_model': 'hr.applicant',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': False,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_send_email_letter(self):
        lst = ['job_id', 'availability', 'salary_proposed']
        missing_fields = []
        for field_name in lst:
            if not getattr(self, field_name, False):
                field_string = self._fields[field_name].string
                missing_fields.append(field_string)
        if missing_fields:
            fields_string = ', '.join(missing_fields)
            raise UserError(_('Missing required fields: %s') % fields_string)

        template_id = self.env.ref('ts_hr_letters.email_template_send_email').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        template = self.env['mail.template'].browse(template_id)
        ctx = {
            'default_model': 'hr.applicant',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': False,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


class HRJob(models.Model):
    _inherit = "hr.job"

    notice_period = fields.Selection([('one month', 'One Month'), ('two month', 'Two Month'),
                                      ('Three month', 'Three Month')], string='Notice Period')