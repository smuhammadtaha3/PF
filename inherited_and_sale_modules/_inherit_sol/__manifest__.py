{
    'name': 'Sale Order Customization',
    'summary': 'Module to add custom fields and functionality in sale order line to sale orders',
    'description': """
    this modile adds a custom discount""",
    'version': '18.0.1.0.0',
    'category': 'Sales Management',
    'author': 'Taha',
    'depends': ['sale_management', 'mail'],
    'data': [

        'views/sale_order_views.xml',

    ],
    'installable': True,
    'application': False,
}
