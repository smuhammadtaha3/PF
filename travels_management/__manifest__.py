{
    'name': 'Travels Management',
    'version': '1.0.0',
    'description': 'The Travels Management',
    'summary': 'The Travels Management',
    'category': 'All',
    'depends': ['base', 'web', 'contacts','mail'],
    'data': [
        'security/ir.model.access.csv',
        'view/travels_management_views.xml',
        'data/data.xml',
        'data/email_template.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
