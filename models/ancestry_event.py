from odoo import api, fields, models

class AncestryEvent(models.Model):
    _name = 'ancestry.event'
    _description = 'Model to represent an event in a tree member\'s life'

    #event info
    # title = fields.Char(string="Event", required=True)
    event_type = fields.Selection([
        ('birth','Birth'),
        ('death','Death'),
        ('marriage','Marriage'),
        ('divorce','Divorce'),
        ('custom','Custom Event')],
        string='Event Type',
        required=True)
    event_custom_label = fields.Char(string="Custom Label")
    event_spouse = fields.Char(string="Spouse") #TODO: change into ancestry.tree.member many2many
    event_date = fields.Date(string="Event Date", required=True)
    event_location = fields.Char(string="Event Location")
    event_description = fields.Text(string="Event Description")
    
    #technical
    status = fields.Selection([("unconfirmed","Unconfirmed"),("confirmed","Confirmed")], string="Status", default="unconfirmed")
    tree_member_id = fields.Many2one(string="Tree ID", comodel_name="ancestry.tree.member")

    def confirm_ancestry_event(self):
        # ensure default not selected
        self.ensure_one()
        assert self.event_type != ""
        # assign tree member id
        member_id = self.env.context.get('active_id')
        self.tree_member_id = self.env['ancestry.tree.member'].search([('id', '=', member_id)])
        # change status to confirmed
        self.status = "confirmed"

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