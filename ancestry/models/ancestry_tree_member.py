from odoo import api, fields, models

class AncestryTreeMember(models.Model):
    _name = 'ancestry.tree.member'
    _description = 'Model to represent a member of a family tree'

    #primary info
    name = fields.Char(string='Name', default='New', required=True)
    family_name = fields.Char(string='Family Name', compute='_compute_family_name')
    suffix = fields.Char(string='Suffix')
    gender = fields.Selection([('female','Female'),('male','Male'),('other','Other')], string='Gender', default='')
    description = fields.Text(string='Description/Summary')
    date_birth = fields.Date(string='Birth')
    date_death = fields.Date(string='Death')
    location_birth = fields.Char(string='Birth Location')
    location_death = fields.Char(string='Death Location')
    is_deceased = fields.Boolean(string='Is Deceased')

    #family relations
    mother = fields.Many2one(
        string='Mother', 
        comodel_name='ancestry.tree.member')
    father = fields.Many2one(
        string='Father', 
        comodel_name='ancestry.tree.member')
    children = fields.Many2many(
        string='Children', 
        comodel_name='ancestry.tree.member', 
        relation='children', 
        column1='parent', 
        column2='child', 
        compute='_compute_children')
    siblings = fields.Many2many(
        string='Siblings', 
        comodel_name='ancestry.tree.member', 
        relation='siblings',
        column1='member', 
        column2='sibling',
        compute='_compute_siblings')
    spouses = fields.Many2many(
        string='Spouses', 
        comodel_name='ancestry.tree.member', 
        relation='spouses', 
        column1='member', 
        column2='spouse')

    #additional info
    events = fields.One2many(string='Life Events', comodel_name='ancestry.event', inverse_name='tree_member_id')
    sources = fields.One2many(string='Sources', comodel_name='ancestry.source', inverse_name='tree_member_id')
    images = fields.One2many(string='Image Gallery', comodel_name='ancestry.media', inverse_name='tree_member_id')

    #technical
    tree_id = fields.Many2one(string='Related Tree', comodel_name='ancestry.tree')
    status = fields.Selection([('unconfirmed','Unconfirmed'),('confirmed','Confirmed')], string='Status', default='unconfirmed')

    #----------------------------------------------------------#

    # Copy family name from tree object to all members
    def _compute_family_name(self):
        for member in self:
            member.family_name = member.tree_id.family_name
    
    # Retrieve the siblings for the current record by matching the mother's 
    # id and father's id of all records to the current record's id
    def _compute_children(self):
        self.children = self.env['ancestry.tree.member'].search([('mother.id', '=', self.id)]) \
            + self.env['ancestry.tree.member'].search([('father.id', '=', self.id)])

    # Retrieve the siblings for the current record by matching the current record's
    # mother's id and father's id to the mother's id and father's id of all records,
    # ensuring that the current record isn't listed as a sibling of itself
    def _compute_siblings(self):
        self.siblings = self.env['ancestry.tree.member'].search(['&', ('mother.id', '=', self.mother.id), ('id', '!=', self.id)]) \
            + self.env['ancestry.tree.member'].search(['&', ('father.id', '=', self.father.id), ('id', '!=', self.id)])
    
    #----------------------------------------------------------#
    
    @api.model_create_multi
    def create(self, vals):
        res = super(AncestryTreeMember, self).create(vals)
        parent_id = res.env.context.get('active_id')
        res.tree_id = self.env['ancestry.tree'].search([('id', '=', parent_id)])
        res.status = 'confirmed'
        return res

    def show_related_tree(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Member',
            'res_model': 'ancestry.tree',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': self.tree_id.id,
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
        }