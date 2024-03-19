from odoo import api, fields, models, _
import json
from odoo.exceptions import ValidationError


class MergeRecords(models.TransientModel):
    _name = 'merge.records'
    _description = 'Merge Records'

    opportunity_ids = fields.Many2many('crm.lead', 'merge_records_rel', 'rec_id', 'lead_id', string='Leads')
    lead_id = fields.Many2one('crm.lead', string='Lead to Keep', domain="[('id', 'in', opportunity_ids)]")
    merge_record_type = fields.Selection([('keep_a_remove_b', 'Keep One Remove Others'),
                                          ('combination', 'Custom Combination')], string='Merge Type')

    radio_name = fields.Selection(selection=lambda self: self._get_lead_name(), string='Lead Names')
    # radio_probability = fields.Selection(selection=lambda self: self._get_lead_probability(), string='Lead probability')
    radio_email = fields.Selection(selection=lambda self: self._get_lead_email(), string='Lead Emails')
    radio_contact_name = fields.Selection(selection=lambda self: self._get_lead_contact(), string='Lead Contact Name')
    radio_phones = fields.Selection(selection=lambda self: self._get_lead_phones(), string='Lead Phones')
    radio_user = fields.Selection(selection=lambda self: self._get_lead_users(), string='Lead Salesperson')
    radio_team = fields.Selection(selection=lambda self: self._get_lead_teams(), string='Lead Teams')
    radio_partner_id = fields.Selection(selection=lambda self: self._get_lead_partner_id(), string='Lead Partner Id')
    radio_partner_name = fields.Selection(selection=lambda self: self._get_lead_partner_name(), string='Lead Partner Name')
    radio_street = fields.Selection(selection=lambda self: self._get_lead_street(), string='Lead Street')
    radio_website = fields.Selection(selection=lambda self: self._get_lead_website(), string='Lead Website')
    radio_function = fields.Selection(selection=lambda self: self._get_lead_function(), string='Lead Function')
    radio_mobile = fields.Selection(selection=lambda self: self._get_lead_mobile(), string='Lead Mobile')

    # @api.onchange('opportunity_ids')
    # def _onchange_opportunity_ids(self):
    #     sorted_opportunity_ids = sorted(self.opportunity_ids, key=lambda lead: lead.create_date)
    #     self.lead_id = sorted_opportunity_ids

    # @api.onchange('lead_id')
    # def onchange_lead_id(self):
    #     if self.lead_id:
    #         for line in self.opportunity_ids.ids:
    #             # raise ValidationError(_('Lines IDS: %s' % line))
    #
    #             if line == self.lead_id.id:
    #                 crm_id = self.env['crm.lead'].browse(line)
    #                 if crm_id:
    #                     crm_id.write({'actives': True})

    @api.model
    def _get_lead_partner_id(self):
        lead_partner_id = []
        unique_partner_id = set()
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            for lead in leads:
                if lead.partner_id and lead.partner_id.id not in unique_partner_id:
                    partner_id = lead.partner_id.id
                    partner_name = lead.partner_id.name
                    lead_partner_id.append((partner_id, partner_name))
                    unique_partner_id.add(partner_id)
        return lead_partner_id

    @api.model
    def _get_lead_teams(self):
        lead_teams = []
        unique_team_ids = set()
        record_ids = self._context.get('active_ids')
        if record_ids:
            # a = self.env['hr.employee'].search_count([('name', '=', self.name)])
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            for lead in leads:
                if lead.team_id and lead.team_id.id not in unique_team_ids:
                    team_id = lead.team_id.id
                    team_name = lead.team_id.name
                    lead_teams.append((team_id, team_name))
                    unique_team_ids.add(team_id)
        return lead_teams

    @api.model
    def _get_lead_users(self):
        lead_users = []
        unique_user_ids = set()
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            for lead in leads:
                if lead.user_id and lead.user_id.id not in unique_user_ids:
                    user_id = lead.user_id.id
                    user_name = lead.user_id.name
                    lead_users.append((user_id, user_name))
                    unique_user_ids.add(user_id)
        return lead_users

    @api.model
    def _get_lead_name(self):
        lead_names = []
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            for lead in leads:
                lead_names.append((lead.name, lead.name))
        return lead_names

    @api.model
    def _get_lead_email(self):
        lead_email = []
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            email_count = {}
            for lead in leads:
                if lead.email_from:
                    email_from = lead.email_from
                    if email_from in email_count:
                        email_count[email_from] += 1
                        email_from = f"{lead.email_from} ({email_count[email_from]})"
                    else:
                        email_count[email_from] = 1
                    lead_email.append((lead.email_from, email_from))
        return lead_email

    @api.model
    def _get_lead_contact(self):
        lead_contact = []
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            contact_count = {}
            for lead in leads:
                if lead.contact_name:
                    contact_name = lead.contact_name
                    if contact_name in contact_count:
                        contact_count[contact_name] += 1
                        contact_name = f"{lead.contact_name} ({contact_count[contact_name]})"
                    else:
                        contact_count[contact_name] = 1
                    lead_contact.append((lead.contact_name, contact_name))
        return lead_contact

    @api.model
    def _get_lead_phones(self):
        lead_phone = []
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            phone_count = {}
            for lead in leads:
                if lead.phone:
                    phone = lead.phone
                    if phone in phone_count:
                        phone_count[phone] += 1
                        phone = f"{lead.phone} ({phone_count[phone]})"
                    else:
                        phone_count[phone] = 1
                    lead_phone.append((lead.phone, phone))
        return lead_phone

    @api.model
    def _get_lead_website(self):
        lead_website = []
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            website_count = {}
            for lead in leads:
                if lead.website:
                    phone = lead.website
                    if phone in website_count:
                        website_count[phone] += 1
                        phone = f"{lead.website} ({website_count[phone]})"
                    else:
                        website_count[phone] = 1
                    lead_website.append((lead.website, phone))
        return lead_website


    @api.model
    def _get_lead_function(self):
        lead_function = []
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            function_count = {}
            for lead in leads:
                if lead.function:
                    phone = lead.function
                    if phone in function_count:
                        function_count[phone] += 1
                        phone = f"{lead.function} ({function_count[phone]})"
                    else:
                        function_count[phone] = 1
                    lead_function.append((lead.function, phone))
        return lead_function

    @api.model
    def _get_lead_mobile(self):
        lead_mobile = []
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            mobile_count = {}
            for lead in leads:
                if lead.mobile:
                    phone = lead.mobile
                    if phone in mobile_count:
                        mobile_count[phone] += 1
                        phone = f"{lead.mobile} ({mobile_count[phone]})"
                    else:
                        mobile_count[phone] = 1
                    lead_mobile.append((lead.mobile, phone))
        return lead_mobile

    @api.model
    def _get_lead_street(self):
        lead_street = []
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            street_count = {}
            for lead in leads:
                if lead.street:
                    phone = lead.street
                    if phone in street_count:
                        street_count[phone] += 1
                        phone = f"{lead.mobile} ({street_count[phone]})"
                    else:
                        street_count[phone] = 1
                    lead_street.append((lead.street, phone))
        return lead_street

    @api.model
    def _get_lead_partner_name(self):
        lead_partner_name = []
        record_ids = self._context.get('active_ids')
        if record_ids:
            leads = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100)
            lead_partner = {}
            for lead in leads:
                if lead.partner_name:
                    phone = lead.partner_name
                    if phone in lead_partner:
                        lead_partner[phone] += 1
                        phone = f"{lead.mobile} ({lead_partner[phone]})"
                    else:
                        lead_partner[phone] = 1
                    lead_partner_name.append((lead.street, phone))
        return lead_partner_name


    def create_new_record(self):
        for rec in self:
            if rec.radio_phones == False:
                phone = 'None'
            else:
                phone = rec.radio_phones
            if rec.radio_email == False:
                email = 'None'
            else:
                email = rec.radio_email
            if rec.radio_contact_name == False:
                contact = 'None'
            else:
                contact = rec.radio_contact_name


            new_record_values = {
                'name': rec.radio_name,
                'email_from': email,
                'phone': phone,
                'contact_name': contact,
            }
            print('------dic--', new_record_values)
            new_record = self.env['crm.lead'].create(new_record_values)
            record_ids = rec._context.get('active_ids')
            original_records = self.env['crm.lead'].browse(record_ids)
            original_records.unlink()
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': new_record.id,
                'view_mode': 'form',
                'view_id': False,
                'target': 'current',
            }


    @api.model
    def default_get(self, fields):
        record_ids = self._context.get('active_ids')
        result = super(MergeRecords, self).default_get(fields)
        if record_ids:
            if 'opportunity_ids' in fields:
                opp_ids = self.env['crm.lead'].browse(record_ids).filtered(lambda opp: opp.probability < 100).ids
                result['opportunity_ids'] = [(6, 0, opp_ids)]
        return result

    def merge_records(self):
        if self.lead_id and self.lead_id.id in self.opportunity_ids.ids:
            # lead_name = self.opportunity_ids[0].name or self.opportunity_ids[1].name
            lead_email = self.opportunity_ids[0].email_from or self.opportunity_ids[1].email_from
            lead_phone = self.opportunity_ids[0].phone or self.opportunity_ids[1].phone
            lead_type = self.opportunity_ids[0].type or self.opportunity_ids[1].type
            lead_contact = self.opportunity_ids[0].contact_name or self.opportunity_ids[1].contact_name
            lead_user = self.opportunity_ids[0].user_id.id or self.opportunity_ids[1].user_id.id
            lead_team = self.opportunity_ids[0].team_id.id or self.opportunity_ids[1].team_id.id
            lead_probability = self.opportunity_ids[0].probability or self.opportunity_ids[1].probability
            lead_partner_id = self.opportunity_ids[0].partner_id.id or self.opportunity_ids[1].partner_id.id
            lead_partner_name = self.opportunity_ids[0].partner_name or self.opportunity_ids[1].partner_name
            lead_website = self.opportunity_ids[0].website or self.opportunity_ids[1].website
            lead_function = self.opportunity_ids[0].function or self.opportunity_ids[1].function
            lead_mobile = self.opportunity_ids[0].mobile or self.opportunity_ids[1].mobile
            lead_description = self.opportunity_ids[0].description or self.opportunity_ids[1].description
            lead_campaign_id = self.opportunity_ids[0].campaign_id or self.opportunity_ids[1].campaign_id
            lead_medium = self.opportunity_ids[0].medium_id or self.opportunity_ids[1].medium_id
            lead_source_id = self.opportunity_ids[0].source_id or self.opportunity_ids[1].source_id
            lead_referred = self.opportunity_ids[0].referred or self.opportunity_ids[1].referred
            lead_date_open = self.opportunity_ids[0].date_open or self.opportunity_ids[1].date_open
            lead_date_close = self.opportunity_ids[0].date_closed or self.opportunity_ids[1].date_closed
            # merged_follower_ids = [(4, id) for id in set(self.opportunity_ids[0].message_follower_ids.ids + self.opportunity_ids[1].message_follower_ids.ids)]
            merged_activity_ids = [(4, id) for id in set(self.opportunity_ids[0].activity_ids.ids + self.opportunity_ids[1].activity_ids.ids)]
            merged_message_ids = [(4,id) for id in set(self.opportunity_ids[0].message_ids.ids +  self.opportunity_ids[1].message_ids.ids)]



            phone = lead_phone if lead_phone else 'None'
            mail = lead_email if lead_email else 'None'
            contact = lead_contact if lead_contact else 'None'
            type = lead_type if lead_type else 'None'

            # selected_record = self.env['crm.lead'].browse(self._context.get('active_ids')[0])
            selected_record = self.env['crm.lead'].browse(self.lead_id.id)

            # Update the selected record with merged data
            selected_record.update({
                # 'name': lead_name,
                'email_from': mail,
                'phone': phone,
                'type': type,
                'contact_name': contact,
                'user_id': lead_user,
                'team_id': lead_team,
                'partner_id': lead_partner_id,
                'partner_name': lead_partner_name,
                'probability': lead_probability,
                'website': lead_website,
                'function': lead_function,
                'mobile': lead_mobile,
                'description': lead_description,
                'campaign_id': lead_campaign_id,
                'medium_id': lead_medium,
                'source_id': lead_source_id,
                'referred': lead_referred,
                'date_open': lead_date_open,
                'date_closed': lead_date_close,
                'activity_ids': merged_activity_ids,
                'message_ids': merged_message_ids,
             })

            # Delete other selected records
            selected_records_to_delete = self.env['crm.lead'].browse(self._context.get('active_ids')[1:])
            print('selected_records_to_delete',selected_records_to_delete)
            selected_records_to_delete.unlink()

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'crm.lead',
                'res_id': selected_record.id,
                'view_mode': 'form',
                'view_id': False,
                'target': 'current',
            }



    # For Dynamic Fields
    # radio_char_fields = fields.Selection(selection=lambda self: self._get_char_fields(), string='Char Fields')
    #
    # def _get_dynamic_base_fields(self):
    #     base_fields = {}
    #     for field_name, field in self.env['crm.lead']._fields.items():
    #         print('field name---->', field_name)
    #         if isinstance(field, fields.Field):
    #             base_fields[field_name] = field.string
    #             print('string---->', base_fields[field_name])
    #     return base_fields
    #
    # @api.model
    # def _get_char_fields(self):
    #     print('cahr--')
    #     return self._get_dynamic_base_fields()




