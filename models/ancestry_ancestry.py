from odoo import api, fields, models

class AncestryAncestry(models.Model):
    _name = 'ancestry.ancestry'
    _description = 'Base model for the Ancestry application'

    family_name = fields.Char(string="Family Name", default="New")
    family_description = fields.Text(string="Family Description")
    display_name = fields.Char(string="Display Name", compute="_compute_display_name")
    
    def _compute_display_name(self):
        for record in self:
            if record.family_name:
                record.display_name = record.family_name

    client = fields.Many2one(string="Client", comodel_name="res.partner")
    family_tree = fields.Many2one(string="Family Tree", comodel_name="ancestry.tree")
