# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'project_team',
    'version': '1.0',
    'summary': "Project team member module",
    'sequence': 16,
    'author': "anand",
    'description': """
Project Team module
""",
    'category': 'Custom/Project',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['mail', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/project.team.member.csv',
        'data/project.team.csv',
        'data/demo_data.xml',
        'wizard/add_to_team.xml',
        'views/menu.xml',
        'views/city.xml',
        'views/project_team.xml',
    ],
    'demo': ['demo/demo.xml'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
