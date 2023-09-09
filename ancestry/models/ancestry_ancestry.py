from odoo import api, fields, models

class AncestryAncestry(models.Model):
    _name = 'ancestry.ancestry'
    _description = 'Base model for the Ancestry application'

    # primary info
    family_name = fields.Char(string="Family Name", default="New", required=True)
    family_description = fields.Text(string="Family Description")
    display_name = fields.Char(string="Display Name", compute="_compute_display_name")
    client = fields.Many2one(string="Client", comodel_name="res.partner", required=True)
    family_tree = fields.Many2one(string="Family Tree", comodel_name="ancestry.tree")
    record_date = fields.Date(string="Date", required=True)

    # analytics
    count_people = fields.Integer(string="Number of People", compute="_compute_count_people")
    count_records = fields.Integer(string="Number of Records", compute="_compute_count_records")
    count_events = fields.Integer(string="Number of Events", compute="_compute_count_events")
    count_photos = fields.Integer(string="Number of Photos", compute="_compute_count_photos")
    count_stories = fields.Integer(string="Number of Stories", compute="_compute_count_stories")
    count_audio = fields.Integer(string="Number of Audio", compute="_compute_count_audio")
    count_videos = fields.Integer(string="Number of Videos", compute="_compute_count_videos")
    count_sources = fields.Integer(string="Number of Sources", compute="_compute_count_sources")
    invited_clients = fields.Many2many(string="Invited Clients", comodel_name="res.partner", relation="invited_clients", column1="tree_id", column2="client_id")

    #technical
    status = fields.Selection([("unconfirmed","Unconfirmed"),("confirmed","Confirmed")], string="Status", default="unconfirmed")

    def _compute_display_name(self):
        for record in self:
            if record.family_name:
                record.display_name = record.family_name
    def _compute_count_people(self):
        for record in self:
            record.count_people = len(record.family_tree.family_members)
    def _compute_count_records(self):
        for record in self:
            record.count_records = record.count_events + record.count_photos + record.count_stories + record.count_audio + record.count_videos + record.count_sources
    def _compute_count_events(self):
        for record in self:
            evt = 0
            for member in record.family_tree.family_members:
                evt += len(member.events)
            record.count_events = evt
    def _compute_count_photos(self):
        for record in self:
            img = 0
            for member in record.family_tree.family_members:
                img += len(member.media.filtered(lambda i: i.media_type == 'photo'))
            record.count_photos = img
    def _compute_count_stories(self):
        for record in self:
            st = 0
            for member in record.family_tree.family_members:
                st += len(member.media.filtered(lambda i: i.media_type == 'story'))
            record.count_stories = st
    def _compute_count_audio(self):
        for record in self:
            aud = 0
            for member in record.family_tree.family_members:
                aud += len(member.media.filtered(lambda i: i.media_type == 'audio'))
            record.count_audio = aud
    def _compute_count_videos(self):
        for record in self:
            vid = 0
            for member in record.family_tree.family_members:
                vid += len(member.media.filtered(lambda i: i.media_type == 'video'))
            record.count_videos = vid
    def _compute_count_sources(self):
        for record in self:
            src = 0
            for member in record.family_tree.family_members:
                src += len(member.sources)
            record.count_sources = src

    @api.model_create_multi
    def create(self, vals):
        # Make new tree
        res = super(AncestryAncestry, self).create(vals)
        res.family_tree = self.env['ancestry.tree'].create({'ancestry_base': res})
        res.status = 'confirmed'
        # Add client to tree as member
        root = self.env['ancestry.tree.member'].create({
            'name': res.client.display_name,
            'family_name': res.family_name,
            'tree_id': res.family_tree.id,
        })
        res.family_tree.family_members = [(4, root.id)]
        res.family_tree.root_member = root
        return res