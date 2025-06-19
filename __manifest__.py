# hospital_management/__manifest__.py
{
    'name': 'Hospital Management',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Module to manage patient data in a hospital',
    'description': 'This module is used for managing patient data, appointments, and medical records.',
    'author': 'Zeeshan Jaffer',
    'depends': ['base', 'mail'],
    'data': [

        'security/ir.model.access.csv',

        'views/hospital_management_patient_views.xml',

        'data/email_template.xml',
        
        'data/email_update_template.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
