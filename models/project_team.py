from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import xlwt


class ProjectTeam(models.Model):
    _name = 'project.team'
    _description = "Project Team"
    _order = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True, translate=True)
    team_members = fields.Many2many('project.team.member', tracking=True)
    team_leader = fields.Many2one('project.team.member', string="Team Leader", tracking=True)
    active = fields.Boolean(default=True)
    sequence = fields.Char(string='Sequence ID', readonly=True, copy=False, tracking=True,
                           default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('sequence', _("New")) == _("New"):
            # Generate sequence number with the format "001/name/date"
            sequence_number = self._generate_sequence_number(vals.get('name', 'Name'))
            vals['sequence'] = sequence_number or _("New")

        result = super(ProjectTeam, self).create(vals)
        return result

    def open_team_members(self):
        action = self.env.ref('project_team.action_open_team_members').read()[0]
        team_member_ids = self.team_members.ids
        team_leader_id = self.team_leader.id
        action['domain'] = ['|', ('id', 'in', team_member_ids), ('id', '=', team_leader_id)]
        return action

    def _generate_sequence_number(self, team_name):
        # Get the current date in YYYYMMDD format
        current_date = fields.Date.today().strftime("%Y%m%d")

        # Find the next sequence number for the team
        next_sequence_number = self.env['ir.sequence'].next_by_code('project.team.sequence') or '001'

        # Format the sequence number as "001/name/date"
        sequence_number = "{:03d}/{}/{}".format(int(next_sequence_number), team_name, current_date)

        return sequence_number

    # def add_member_wizard_action(self):
    #     view_id = self.env.ref('project_team.view_add_member_wizard_form').id
    #     print(view_id, 'iiiiiiiiiiiiii')
    #     return {
    #         'name': 'action_add_member',
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'res_model': 'add.member.wizard',
    #         'target': 'new',
    #         'view_id': view_id,
    #         'views': [(view_id, 'form')],
    #         'res_id': self.env['add.member.wizard']['name'].id,
    #         'context': self.env.context,
    #         'domain': [],
    #     }

    def add_member_wizard_action(self):
        action = self.env.ref('project_team.action_add_member').read()[0]
        print(action, 'oooooooooooooooooooooooooooooo')
        return action


class ProjectTask(models.AbstractModel):
    _inherit = 'project.task'

    assigned_date = fields.Datetime(string='Assigned Date')

    @api.model
    def create(self, vals):
        if 'assigned_date' in vals:
            assigned_date = fields.Datetime.to_datetime(vals['assigned_date'])
            if assigned_date < fields.Datetime.now():
                raise ValidationError('Assigned date is invalid! Please provide a correct date.')
        return super(ProjectTask, self).create(vals)

    def write(self, vals):
        if 'assigned_date' in vals:
            assigned_date = fields.Datetime.to_datetime(vals['assigned_date'])
            if assigned_date < fields.Datetime.now():
                raise ValidationError('Assigned date is invalid! Please provide a correct date.')
        return super(ProjectTask, self).write(vals)

    def unlink(self):
        for i in self:
            if i.stage_id.name == 'In Progress':
                raise ValidationError(_("Can not delete the record!"))
            else:
                return super(ProjectTask, i).unlink()

    def give_priority(self):
        print("Priority----------------")
        selected_records = self.env['project.task'].search([('id', 'in',
                                                             list(self.env.context.get('active_ids')))])
        print(selected_records)
        for i in selected_records:
            i.write({'priority': '1'})


class ProjectProject(models.Model):
    _inherit = 'project.project'

    team_id = fields.Many2one('project.team', string="Project Team")
    team_ids = fields.Many2many('project.team', string="Teams")

