from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)  # Logger for better debugging


class HospitalManagementPatient(models.Model):
    _name = 'hospital.management.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # <-- VERY IMPORTANT
    _description = 'Patient'

    _track = True
    name = fields.Char(string="Name", required=True, tracking=True, track_visibility='onchange')
    email = fields.Char(string="Email", required=True,
                        tracking=True)  # Email is now required
    lang = fields.Selection(
        selection=lambda self: self.env['res.lang'].get_installed(),
        string="Language",
        help="The language used for emails and notifications."
    )
    

    partner_id = fields.Many2one('res.partner', string="Partner")

    address = fields.Text(string="Address", tracking=True)
    country_id = fields.Many2one(
        'res.country', string="Country", tracking=True)  # Country dropdown
    state_id = fields.Many2one('res.country.state', string="State",
                                # State filtered by country
                                domain="[('country_id', '=', country_id)]", tracking=True)
    age = fields.Integer(string="Age", tracking=True)
    #  newly added field
    age_category = fields.Char(string="Age Category", compute="compute_age_category", store=True, help="Age category based on patient's age"
                                "helloo ", tracking=True)
    # age_category = fields.Selection(
    #     [('child', 'Child'), ('adult', 'Adult'), ('senior', 'Senior')], string="Age Category", tracking=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True)
    hobbies = fields.Selection(
        [('cricket', 'Cricket'), ('hockey', 'Hockey'), ('badminton', 'Badminton')], string="Hobbies", tracking=True)

    medical_history = fields.Text(string="Medical History", tracking=True)

    # To store patient's medical condition
    diagnosis = fields.Text(string="Diagnosis", tracking=True)
    # To store ongoing treatment details
    treatment = fields.Text(string="Treatment Dr. Name", compute="manage_dr_name",store=True, tracking=True)
    # To store prescribed medication
    medications = fields.Text(string="Prescribed Medications", compute="compute_medications",
                                store=True, tracking=True)
    image = fields.Image(string="Patient Image", max_width=128, max_height=128, tracking=True)
    
    status = fields.Selection([
        ("new", "New"),

        ("recovered", "Recovered"),
        ("discharged", "Discharged"),
    ], default="new", tracking=True)

    def action_new(self):
        self.write({'status': 'new'})

    def action_recovered(self):
        self.write({'status': 'recovered'})

    def action_discharged(self):
        self.write({'status': 'discharged'})
    
    @api.depends('age')
    def compute_age_category(self): # newly added method
        """ Compute the age category based on the age of the patient. """	
        for record in self:
            if record.age < 18:
                record.age_category = 'Child'
            elif 18 <= record.age < 60:
                record.age_category = 'Adult'
            else:
                record.age_category = 'Senior'

    @api.depends('medications')
    def company_medications(self):
        """ Compute the medications based on the patient's medical history. """
        for record in self:
            if record.medical_history:
                if 'diabetes' in record.medical_history.lower():
                    record.medications = 'Metformin'
                elif 'hupertenseion' in record.medical_history.lower():
                    record.medications = 'lisinopril'
                else:
                    record.medications = 'No specific medications prescribed'
            else:
                record.medications = 'No medical history available'
                
                
    @api.onchange('age', 'gender')
    def manage_dr_name(self):
        """ Compute the doctor's name based on the patient's age and gender. """
        for record in self:
            if record.age < 18:
                if record.gender == 'male':
                    record.treatment = 'Dr. Naheez'
                else:
                    record.treatment = 'Dr. Shahida'
            elif 18 <= record.age < 60:
                if record.gender == 'male':
                    record.treatment = 'Dr. Ali'
                else:
                    record.treatment = 'Dr. Fatima'
            else:
                if record.gender == 'male':
                    record.treatment = 'Dr. Ahmed'
                else:
                    record.treatment = 'Dr. Sarah'
        
    @api.ondelete(at_uninstall=False)
    def check_criteria(self):
        """
        Check if the patient record meets the criteria for deletion.
        If the criteria are not met, raise a UserError.
        """
        for record in self:
            if record.status != 'discharged':
                raise UserError("You cannot delete a patient record that is not discharged.")
            # Add any other criteria checks here
            else:
                if (record.age or record.gender or record.name or record.email):
                    raise UserError("You cannot delete a patient record if age or gender is provided.")
    
    
    def _send_creation_email(self):
        if self.email:
            try:
                # Get the email template
                template = self.env.ref(
                    'hospital_management.patient_creation_success_template')
                if not template:
                    _logger.error(
                        "Email template 'hospital_management.patient_creation_success_template' not found!")
                    raise UserError("Email template not found!")

                # ✅ The modern, correct method
                template.send_mail(self.id, force_send=True)

                # Log the email sending in the chatter
                self.message_post(
                    body=f"Email sent successfully to {self.email}",
                    subject="Email Notification",
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )
                _logger.info(
                    f"Email sent successfully to {self.email} for patient {self.name}")

            except Exception as e:
                _logger.error(
                    f"Error sending email to {self.email} for patient {self.name}: {e}")
                self.env.cr.rollback()
                raise UserError(f"Error sending email: {e}")
        else:
            _logger.warning(
                f"Patient {self.name} has no email address. Skipping email.")

    @api.model
    def _get_display_name(self, field):
        return self._fields[field].string if field in self._fields else field

    def send_update_email(self):
        for rec in self:
            message = "<h3>Updated Patient Record</h3><ul>"
            for field_name, field in rec._fields.items():
                if not field.store or field_name in ['id', '__last_update', 'create_date', 'create_uid', 'write_date', 'write_uid']:
                    continue
                try:
                    value = rec[field_name]
                    if field.type in ['many2one']:
                        value_display = value.name if value else ''
                    elif field.type in ['one2many', 'many2many']:
                        value_display = ', '.join(val.display_name for val in value)
                    else:
                        value_display = value or ''
                    label = field.string or field_name
                    message += f"<li><strong>{label}:</strong> {value_display}</li>"
                except Exception:
                    continue
            message += "</ul>"

            template = self.env.ref('hospital_management.patient_record_update_template', raise_if_not_found=False)
            if not template:
                raise UserError("Email template not found with ID 'hospital_management.patient_record_update_template'.")

            # Clone the template to avoid modifying it
            template_copy = template.copy()
            template_copy.email_to = rec.create_uid.partner_id.email or ''
            template_copy.body_html = message
            template_copy.send_mail(rec.id, force_send=True)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Update email has been sent successfully!',
                'type': 'success',
                'sticky': False,
            }
        }

    @api.model
    def write(self, vals):
        # Track changes before writing
        old_values = {
            rec.id: {field: rec[field] for field in vals.keys() if field in rec._fields}
            for rec in self
        }
        
        result = super(HospitalManagementPatient, self).write(vals)
        
        # Prepare changed fields data
        changes = {}
        for rec in self:
            rec_changes = {}
            for field, new_value in vals.items():
                if field not in rec._fields:
                    continue
                old_value = old_values[rec.id].get(field)
                if old_value != new_value:
                    rec_changes[field] = {
                        'field_name': rec._fields[field].string,
                        'old': old_value,
                        'new': new_value
                    }
            if rec_changes:
                changes[rec.id] = rec_changes
        
        # Send notifications
        if changes:
            for rec_id, rec_changes in changes.items():
                template = self.env.ref('hospital_management.patient_record_update_template')
                template.with_context(changes=rec_changes).send_mail(rec_id, force_send=True)
        
        return result

    def create(self, vals):
        patient = super(HospitalManagementPatient, self).create(vals)
        patient._send_creation_email()
        return patient
    
    def _message_auto_thread(self, *args, **kwargs):
        """Override to prevent automatic document threading"""
        return False
    


    # def send_change_notification(self, changes):
    #     """
    #     Sends a notification about changes made to a patient's record.
    #     This method performs the following actions:
    #     1. Sends an email notification to the patient using a predefined email template.
    #     2. Logs the changes in the chatter for the patient's record.
    #     Args:
    #         changes (dict): A dictionary containing the changes made to the records.
    #             The structure of the dictionary is as follows:
    #             {
    #                 record_id: {
    #                     field_name: {
    #                         'field_name': str,  # The human-readable name of the field
    #                         'old': str,         # The old value of the field
    #                         'new': str          # The new value of the field
    #                     },
    #                     ...
    #                 },
    #                 ...
    #             }
    #     Example:
    #         changes = {
    #             1: {
    #                 'name': {
    #                     'field_name': 'Name',
    #                     'old': 'John Doe',
    #                     'new': 'John Smith'
    #                 },
    #                 'age': {
    #                     'field_name': 'Age',
    #                     'old': '30',
    #                     'new': '31'
    #                 }
    #             }
    #         }
    #         self.send_change_notification(changes)
    #     Note:
    #         - The email template used is identified by the XML ID 
    #             'hospital_management.patient_record_update_template'.
    #         - The changes are logged in the chatter with a formatted HTML list.
    #     """
    #     for rec in self:
    #         if rec.id in changes:
    #             # Pass the changes context to the email template
    #             template = self.env.ref('hospital_management.patient_record_update_template')
    #             template.with_context(changes=changes[rec.id]).send_mail(rec.id)

    #             # Log changes in the chatter
    #             change_details = "<ul>"
    #             for field, change in changes[rec.id].items():
    #                 change_details += f"<li><strong>{change['field_name']}:</strong> {change['old']} → {change['new']}</li>"
    #             change_details += "</ul>"

    #             rec.message_post(
    #                 body=f"The following fields were updated:<br/>{change_details}",
    #                 subject="Record Updated",
    #                 message_type="comment",
    #                 subtype_xmlid="mail.mt_comment",
    #             )    
    
    # def unlink(self):
    #     for record in self:
    #         if record.age or record.gender or record.name or record.email:
    #             return {
    #                 'type': 'ir.actions.act_window',
    #                 'name': 'Confirm Deletion',
    #                 'res_model': 'patient.delete.confirm.wizard',
    #                 'view_mode': 'form',
    #                 'target': 'new',
    #                 'context': {'active_id': record.id},
    #             }
    #     return super().unlink()
