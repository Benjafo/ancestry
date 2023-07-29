from odoo import api, fields, models

class AncestrySource(models.Model):
    _name = 'ancestry.source'
    _description = 'Model to represent a file or historical document that is referenced by a tree member\'s profile'

    # title = fields.Char(string="Source", required=True)

    caption = fields.Char(string="Caption", required=True, default="[image caption]")
    file = fields.Binary(string="File", attachment=True)
    file_name = fields.Char(string="File Name")
    
    #technical
    status = fields.Selection([("unconfirmed","Unconfirmed"),("confirmed","Confirmed")], string="Status", default="unconfirmed")
    tree_member_id = fields.Many2one(string="Tree ID", comodel_name="ancestry.tree.member")

    def confirm_ancestry_source(self):
        # ensure default not selected
        self.ensure_one()
        # assert self.source_type != ""
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