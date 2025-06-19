# travels_management.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
import logging
_logger = logging.getLogger(__name__)

class TravelsManagement(models.Model):
    _name = "travels.management"
    _description = "Travels Management"

    name = fields.Char(string="Traveler Name", required=True)
    email = fields.Char(string="Email", required=True)
    booking_reference = fields.Char(string='Booking Reference', readonly=False)
    partner_id = fields.Many2one('res.partner', required=True)
    product_id = fields.Many2one('product.template')
    company_id = fields.Many2one('res.company')
    no_of_passengers = fields.Integer(string="No of Passengers", default=2)
    booking_date = fields.Datetime(string="Booking Date")

    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('confirmed', "Confirmed"),
        ],
        string="Status",
        readonly=False,
        default='draft'
    )

    @api.model  # This is important!
    def create(self, vals_list):
        records = super(TravelsManagement).create(vals_list)
        records._send_creation_email()
        return records
    
    def send_email_confirmation(self):
        """Method to send confirmation email"""
        try:
            template = self.env.ref('travels_management.email_template_travel_confirmation', raise_if_not_found=True) # raise_if_not_found=True

            _logger.info(f"Sending email to: {self.email}")
            _logger.info(f"Using template: {template.name}")

            mail_id = template.send_mail(self.id, force_send=True, raise_exception=True) # raise_exception=True

            _logger.info(f"Email successfully sent. Mail ID: {mail_id}")
        except Exception as e:
            _logger.error(f"Error sending email: {e}")  # Log the actual exception
            
    def _send_creation_email(self):
        if self.email:
            try:
                template = self.env.ref('travels_management.email_template_travel_confirmation')
                if not template:
                    _logger.error("Email template 'travels_management.email_template_travel_confirmation' not found!")
                    raise UserError("Email template not found!")

                mail_values = {
                    'email_to': self.email,  # Use template's subject
                    'subject': template.subject,  # Use template's subject
                    'body_html': template.body_html,  # Use template's body
                    'model': self._name, # set the model
                    'res_id': self.id, # set the record id
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send() # Send the email

                _logger.info(f"Email sent successfully to {self.email} for patient {self.name}")

            except Exception as e:
                _logger.error(f"Error sending email to {self.email} for patient {self.name}: {e}")
                self.env.cr.rollback()  # Rollback on email failure
                raise UserError(f"Error sending email: {e}")
        else:
            _logger.warning(f"traveller {self.name} has no email address. Skipping email.")
    
    def action_send_mail(self):
        template = self.env.ref('travels_management.email_template_travel_confirmation')
        for rec in self:
            if rec.email:
                template.send_mail(rec.id)

    def action_confirm(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'confirmed'
            # record.send_email_confirmation()  # Send email when confirmed
            record._send_creation_email()
            # record.action_send_mail()