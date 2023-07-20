from odoo import api, fields, models

class AncestrySource(models.Model):
    _name = 'ancestry.source'

    # title = fields.Char(string="Source", required=True)

    file = fields.Binary(string="File")
    caption = fields.Char(string="Caption", required=True, default="[image caption]")
    
    #technical
    tree_member_id = fields.Many2one(string="Tree ID", comodel_name="ancestry.tree.member")