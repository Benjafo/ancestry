from odoo import api, fields, models

class AncestryImage(models.Model):
    _name = 'ancestry.image'

    title = fields.Char(string="Image", required=True)
    
    #technical
    tree_member_id = fields.Many2one(string="Tree ID", comodel_name="ancestry.tree.member")