from odoo import api, fields, models

class AncestryTree(models.Model):
    _name = 'ancestry.tree'
    _description = 'Model to represent a family tree and its members'

    family_name = fields.Char(string="Family Name")
    family_members = fields.One2many(string="Family Members", comodel_name="ancestry.tree.member", inverse_name="tree_id")
    display_name = fields.Char(compute="_compute_display_name")

    def _compute_display_name(self):
        for tree in self:
            tree.display_name = tree.family_name + " Tree"

    def add_ancestry_tree_member(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Member',
            'res_model': 'ancestry.tree.member',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
        }

class AncestryTreeMember(models.Model):
    _name = 'ancestry.tree.member'
    _description = 'Model to represent a member of a family tree'

    #primary info
    name = fields.Char(string="Name", default="New", required=True)
    # middle_name = fields.Char(string="Middle Name")
    # last_name = fields.Char(string="Last Name", required=True)
    # suffix = fields.Char(string="Suffix")
    gender = fields.Selection([('female','Female'),('male','Male'),('other','Other')], string='gender', default='other')
    description = fields.Text(string="Description/Summary")
    date_birth = fields.Date(string="Birth")
    date_death = fields.Date(string="Death")
    location_birth = fields.Char(string="Birth Location")
    location_death = fields.Char(string="Death Location")
    is_living = fields.Boolean(string="Is Living")

    #family info
    mother = fields.Many2one(string="Mother", comodel_name="ancestry.tree.member")
    father = fields.Many2one(string="Father", comodel_name="ancestry.tree.member")
    siblings = fields.Many2many("ancestry.tree.member", "siblings", "sibling_one", "sibling_two", string="Siblings")
    spouses = fields.Many2many("ancestry.tree.member", "spouses", 'spouse_one', 'spouse_two', string="Spouses")
    children = fields.One2many(string="Children", comodel_name="ancestry.tree.member", inverse_name="mother", compute="_update_children")

    #additional info
    events = fields.One2many(string="Life Events", comodel_name="ancestry.event", inverse_name="tree_member_id")
    sources = fields.One2many(string="Sources", comodel_name="ancestry.source", inverse_name="tree_member_id")
    images = fields.One2many(string="Image Gallery", comodel_name="ancestry.media", inverse_name="tree_member_id")

    #technical
    tree_id = fields.Many2one(string="Related Tree", comodel_name="ancestry.tree")
    status = fields.Selection([("unconfirmed","Unconfirmed"),("confirmed","Confirmed")], string="Status", default="unconfirmed")
    # is_wizard_view = fields.Boolean(string="Is Wizard View Entry")

    @api.depends("mother")
    def _update_children(self):
        self.children = self.children
        self.mother.children.write(self)
        print(self)

    def confirm_ancestry_tree_member(self):
        self.ensure_one()
        # assign parent tree id
        parent_id = self.env.context.get('active_id')
        self.tree_id = self.env['ancestry.tree'].search([('id', '=', parent_id)])
        # add record to family tree
        # self.tree_id.family_members.write(self)
        # change member status to confirmed
        self.status = 'confirmed'

    def show_related_tree(self):
         # print('uh oh')
         # debug
        #  c = self.env.context
        # tree = self.env.context.get('active_id')
        # t = 
        # open related family tree
        # active = self.env.context.get('active_id')
        # self.is_wizard_view = active
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Member',
            'res_model': 'ancestry.tree',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.tree_id.id,
            # 'domain': [('id', '=', self.tree_id)],
        }
    
    def show_profile(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'View Profile',
            'res_model': 'ancestry.tree.member',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.id,
            # 'domain': [('id', '=', self.tree_id)],
        }