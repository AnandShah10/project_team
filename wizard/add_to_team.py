from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class AddMemberWizard(models.TransientModel):
    _name = 'add.member.wizard'
    _description = 'Wizard to add member to teams'

    name = fields.Many2one('project.team.member', string='Member')

    def action_add_member(self):
        print("hello")
        if self.name:
            project_team_id = self.env.context.get('active_ids')
            project_team = self.env['project.team'].browse(project_team_id)
            if project_team:
                project_team.write({'team_members': [(4, self.name.id)]})
