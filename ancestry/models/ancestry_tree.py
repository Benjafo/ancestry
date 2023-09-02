from odoo import api, fields, models

class AncestryTree(models.Model):
    _name = 'ancestry.tree'
    _description = 'Model to represent a family tree and its members'

    ancestry_base = fields.One2many(string="Ancestry Ref", comodel_name="ancestry.ancestry", inverse_name="family_tree")
    family_name = fields.Char(string="Family Name", compute="_compute_family_name")
    display_name = fields.Char(string="Display Name", compute="_compute_display_name")
    family_members = fields.One2many(string="Family Members", comodel_name="ancestry.tree.member", inverse_name="tree_id")
    root_member = fields.Many2one(string="Root Family Member", comodel_name="ancestry.tree.member")

    def _check_portal(self):
        # Add access rules for the portal users
        return self.env.user.has_group('base.group_portal')

    def _compute_family_name(self):
        for tree in self:
            tree.family_name = tree.ancestry_base.family_name
            
    def _compute_display_name(self):
        for record in self:
            if record.family_name:
                record.display_name = record.family_name + " Tree"

    def add_ancestry_tree_member(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Member',
            'res_model': 'ancestry.tree.member',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
        }

    def create_marriage_link(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Marriage Link',
            'res_model': 'marriage.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }