from odoo import api, fields, models, _
import string, secrets
from odoo.exceptions import ValidationError, UserError


class ProjectTeamMember(models.Model):
    _name = 'project.team.member'
    _description = "Project Team Member"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name:", translate=True)
    address = fields.Text(string="Address:")
    user_id = fields.Many2one('res.users', required=True, string="User ID:",
                              default=lambda self: self.env.context.get('search_default_employee', False))
    email = fields.Char(string="Email Address:", related="user_id.email")
    mobile = fields.Char(string="Mobile No:")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')],
                              string="Gender")
    user_image = fields.Binary(string="Image")
    active = fields.Boolean(default=True)
    dob = fields.Date(string="Date Of Birth:")
    bio_data = fields.Html(string="Bio Data:")
    description = fields.Text(string="Description", index=True)

    timesheet = fields.One2many('account.analytic.line', 'member_ids', string='Time Sheet')

    @api.onchange('addr1', 'addr2', 'country', 'state', 'zip', 'city', 'address', 'house_no')
    def make_address(self):
        for i in self:
            if i.addr1 and i.country and i.state and i.house_no and i.city and i.zip:
                i.address = str(str(i.house_no) + ',' + '\r\n' +
                                str(i.addr1) + ',' + '\r\n' +
                                str(i.addr2) + ',' + '\r\n' +
                                str(i.city.name) + ' - ' + str(i.zip) +
                                ',' + '\r\n' + str(i.state.name) +
                                ',' + str(i.country.name) +
                                '.')

            else:

                i.address = ''

    def generate_password(self, length=12):
        """Generate a random password with the specified length."""
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

    def create_user(self, vals):
        password = self.generate_password()
        print(password)
        """Method to create a new user based on project team member details."""
        user_vals = {
            'name': vals.get('name'),  # Use appropriate fields from your model
            'login': vals.get('name'),  # Assuming email is used for login
            'password': password,  # Set initial password
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
        }
        res = self.env['res.users'].sudo().create(user_vals)
        print("LLLLLLLLLLLLLLLLL")
        return user_vals['password'], res

    @api.model
    def create(self, vals):
        # if vals.get('p_id', _('New')) == _('New'):
        #     vals['p_id'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')

        res = super(ProjectTeamMember, self).create(vals)
        password, x = self.create_user(vals)
        print("III", password, x)
        res.write({'user_id': x})
        print("ccccccccccccccccccc")
        print("PPPPPPPPPPPPPPPP", res)
        return res

    def copy(self, default=None):
        raise UserError("Can Not Copy The record")


class AnalyticLineInherit(models.AbstractModel):
    _inherit = 'account.analytic.line'

    member_ids = fields.Many2one('project.team.member')


# class ProjectInherit(models.AbstractModel):
#     _inherit = 'project.project'
#
#     description = fields.Text(string="Description", index=True,
#                               help="This field is indexed to improve"
#                                    " performance when searching projects by description."
#                               )


class MemberAddress(models.AbstractModel):
    _inherit = 'project.team.member'
    house_no = fields.Char()
    addr1 = fields.Char()
    addr2 = fields.Char()
    zip = fields.Integer()
    country = fields.Many2one('res.country')
    state = fields.Many2one('res.country.state', domain="[('country_id', '=', country)]")
    city = fields.Many2one('res.state.city', string='City', domain="[('state', '=', state)]")
