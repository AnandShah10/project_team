from odoo import api, fields, models, _


class StateCity(models.Model):
    _name = 'res.state.city'
    _description = 'City'

    name = fields.Char(string='City Name')
    country = fields.Many2one('res.country', string='Country')
    state = fields.Many2one('res.country.state', string='State', domain="[('country_id', '=', country)]")
