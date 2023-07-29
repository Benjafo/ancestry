from odoo import api, fields, models
import os

class AncestryMedia(models.Model):
    _name = 'ancestry.media'
    _description = 'Model to represent a piece of media pertaining to a tree member'

    #event info
    media_type = fields.Selection([
        ('photo','Photo'),
        ('story','Story'),
        ('audio','Audio')],
        string='Media Type',
        required=True)
    file = fields.Binary(string="File", attachment=True, required=True)
    file_name = fields.Char(string="File Name")
    title = fields.Char(string="Media Title", required=True)
    media_date = fields.Date(string="Date")
    media_location = fields.Char(string="Location")
    media_description = fields.Text(string="Description")
    
    #technical
    status = fields.Selection([("unconfirmed","Unconfirmed"),("confirmed","Confirmed")], string="Status", default="unconfirmed")
    tree_member_id = fields.Many2one(string="Tree ID", comodel_name="ancestry.tree.member")


    # confirm and assign tree member id upon file upload
    @api.onchange("file")
    def _onchange_ancestry_media(self):
        self.ensure_one()
        # ensure default not selected
        if self.media_type is not False:
            self.status = "confirmed"
            member_id = self.env.context.get('active_id')
            self.tree_member_id = self.env['ancestry.tree.member'].search([('id', '=', member_id)])

    # update default file title
    @api.onchange("file_name")
    def _onchange_file_name(self):
        self.ensure_one()
        # ensure a media type is selected
        if self.media_type is not False:
            self.title = os.path.splitext(self.file_name)[0].capitalize()

    def back_to_profile(self):  
        return {
            'type': 'ir.actions.act_window',
            'name': 'View Profile',
            'res_model': 'ancestry.tree.member',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.tree_member_id.id,
        }