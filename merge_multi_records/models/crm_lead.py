from odoo import fields, models, api, _
from odoo.exceptions import UserError


class CRMLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'CRM Lead'

    actives = fields.Boolean(string='Check')



    # @api.model
    # def _merge_opportunity(self, user_id=False, team_id=False, auto_unlink=True, max_length=5):
    #     """ Override the private merging method to remove the warning about selecting more than one element. """
    #     opportunities = self._sort_by_confidence_level(reverse=True)
    #
    #     if max_length and len(self.ids) > max_length and not self.env.is_superuser():
    #         raise UserError(_("To prevent data loss, Leads and Opportunities can only be merged by groups of %(max_length)s.", max_length=max_length))
    #
    #     opportunities_head = opportunities[0]
    #     opportunities_tail = opportunities[1:]
    #
    #     merged_data = opportunities._merge_data(self._merge_get_fields())
    #
    #     if user_id:
    #         merged_data['user_id'] = user_id
    #     if team_id:
    #         merged_data['team_id'] = team_id
    #
    #     merged_followers = opportunities_head._merge_followers(opportunities_tail)
    #     opportunities_head._merge_log_summary(merged_followers, opportunities_tail)
    #     opportunities_head._merge_dependences(opportunities_tail)
    #
    #     if merged_data.get('team_id'):
    #         team_stage_ids = self.env['crm.stage'].search(['|', ('team_id', '=', merged_data['team_id']), ('team_id', '=', False)], order='sequence, id')
    #         if merged_data.get('stage_id') not in team_stage_ids.ids:
    #             merged_data['stage_id'] = team_stage_ids[0].id if team_stage_ids else False
    #
    #     opportunities_head.write(merged_data)
    #
    #     if auto_unlink:
    #         opportunities_tail.sudo().unlink()
    #
    #     return opportunities_head
    #
    # def _merge_followers(self, opportunities_tail):
    #     # ...
    #     follower_ids = self.opportunities_head.message_follower_ids.ids
    #     for opportunity in opportunities_tail:
    #         follower_ids |= opportunity.message_follower_ids.ids
    #     # ...
    #     self.env.cr.execute(
    #         """DELETE FROM mail_followers
    #            WHERE res_model = %s AND res_id IN %s AND id NOT IN %s""",
    #         (self._name, tuple([opportunity.id for opportunity in opportunities_tail]),
    #          tuple(follower_ids)))