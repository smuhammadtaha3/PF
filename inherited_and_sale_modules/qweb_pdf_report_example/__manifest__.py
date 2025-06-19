{
    'name': 'Qweb PDF Report Example',
    'summary': 'Custom Qweb PDF Report Generation',
    'description': """
        Features:
        - Set discounts on products
        - Custom route to display discounted products
        - Generate PDF reports for discounted products
        - Support for multiple languages
    """,
    'version': '18.0.0.0.2',
    'category': 'Reporting',
    'author': 'Taha',
    'website': 'https://yourwebsite.com',
    'depends': ['hospital_management','base','web'],
    'data': [
        'report/patient_report_template.xml',
        'report/inherit_qweb_template.xml',
        'report/patient_card_template.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}