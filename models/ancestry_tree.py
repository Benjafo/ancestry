from odoo import api, fields, models

class AncestryTree(models.Model):
    _name = 'ancestry.tree'
    _description = 'Model to represent a family tree and its members'

    ancestry_base = fields.One2many(string="Base Ancestry Ref", comodel_name="ancestry.ancestry", inverse_name="family_tree")
    family_name = fields.Char(string="Family Name", compute="_compute_family_name")
    display_name = fields.Char(string="Display Name", compute="_compute_display_name")
    family_members = fields.One2many(string="Family Members", comodel_name="ancestry.tree.member", inverse_name="tree_id")

    def _compute_family_name(self):
        for tree in self:
            tree.family_name = tree.ancestry_base.family_name + " Tree"
            
    def _compute_display_name(self):
        for record in self:
            if record.family_name:
                record.display_name = record.family_name

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
    children = fields.Many2many(string="Children", comodel_name="ancestry.tree.member", relation="children", column1="parent", column2="child")
    siblings = fields.Many2many(string="Siblings", comodel_name="ancestry.tree.member", relation="siblings", column1="member", column2="sibling")
    spouses = fields.Many2many(string="Spouses", comodel_name="ancestry.tree.member", relation="spouses", column1='member', column2='spouse')

    #additional info
    events = fields.One2many(string="Life Events", comodel_name="ancestry.event", inverse_name="tree_member_id")
    sources = fields.One2many(string="Sources", comodel_name="ancestry.source", inverse_name="tree_member_id")
    images = fields.One2many(string="Image Gallery", comodel_name="ancestry.media", inverse_name="tree_member_id")

    #technical
    tree_id = fields.Many2one(string="Related Tree", comodel_name="ancestry.tree")
    status = fields.Selection([("unconfirmed","Unconfirmed"),("confirmed","Confirmed")], string="Status", default="unconfirmed")
    # is_wizard_view = fields.Boolean(string="Is Wizard View Entry")
    # TESTMANY2MANY = fields.Many2many(string="TESTING PURPOSES ONLY", comodel_name="ancestry.tree.member", relation="test_many2many", column1="test_many2many_column1", column2 = "test_many2many_column2")

    #----------------------------------------------------------#
    # TODO:
    # 1. On change of mother or father, remove self from the previous mother or father's children
    # 2. Add function for on change of children, to ensure correct two way functionality (do we want to implement this?)

    @api.onchange("mother")
    def _onchange_mother(self):
        # remove child from previous mother's record
        if self._origin.mother:                         #TODO: why isnt this working?
            self._origin.mother.children -= self        #   <--------------------
        # write child to new mother's record, union operator handles duplicate records
        self.mother.children |= self

    @api.onchange("father")
    def _onchange_father(self):
        # remove child from previous father's record
        if self._origin.father:                         #TODO: why isnt this working?
            self._origin.father.children -= self        #   <--------------------
        # write child to new father's record, union operator handles duplicate records
        self.father.children |= self

    @api.onchange("children")
    def _onchange_children(self):
        print('do we need to implement this functionality?')

    
    def write(self, vals):
        """
        Update many2manys, serves as:
            @api.onchange("siblings")
            @api.onchange("spouses")
        """
        for member in self:
            # update siblings
            if 'siblings' in vals:
                new_siblings = vals['siblings'][0][2] if vals.get('siblings') else []
                existing_siblings = member.siblings.ids
                # add current member to the siblings list of new siblings
                if new_siblings:
                    for new_sibling_id in new_siblings:
                        if new_sibling_id not in existing_siblings:
                            self.env['ancestry.tree.member'].browse(new_sibling_id).write({
                                'siblings': [(4, member.id, 0)]
                            })
                # remove current member from the siblings list of old siblings
                if existing_siblings:
                    for sibling_id in existing_siblings:
                        if new_siblings and sibling_id not in new_siblings:
                            self.env['ancestry.tree.member'].browse(sibling_id).write({
                                'siblings': [(3, member.id, 0)]
                            })
            # update spouses
            if 'spouses' in vals:
                new_spouses = vals['spouses'][0][2] if vals.get('spouses') else []
                existing_spouses = member.spouses.ids
                # add current member to the spouses list of new spouses
                if new_spouses:
                    for new_spouse_id in new_spouses:
                        if new_spouse_id not in existing_spouses:
                            self.env['ancestry.tree.member'].browse(new_spouse_id).write({
                                'spouses': [(4, member.id, 0)]
                            })
                # remove current member from the spouses list of old spouses
                if existing_spouses:
                    for spouse_id in existing_spouses:
                        if new_spouses and spouse_id not in new_spouses:
                            self.env['ancestry.tree.member'].browse(spouse_id).write({
                                'spouses': [(3, member.id, 0)]
                            })
        return super(AncestryTreeMember, self).write(vals)

    #----------------------------------------------------------#

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