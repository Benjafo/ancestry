from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal

class AncestryFamilyTree(CustomerPortal):

    """
    Retrieve ALL data that will be used build the JS representation of the tree,
    format into JSON, and pass to the template view
    """
    @route('/my/tree', type='http', auth="public", website=True)
    def tree(self, **kwargs):
        values = self._prepare_portal_layout_values()
        tree = request.env['ancestry.tree'].sudo().search([('id', '=', kwargs['id'])])
        values.update({'tree_data': self._get_tree_data(tree)})
        return request.render("ancestry.portal_ancestry_record", values)

    def _get_family_member(self, root):
        return {
            "id": root.id,
            "tree_id": root.tree_id.id,
            "name": root.name,
            "status": root.status,
            "date_birth": root.date_birth,
            "date_death": root.date_death,
            "is_living": root.is_living,
            "location_birth": root.location_birth,
            "location_death": root.location_death,
            "description": root.description,
            "gender": root.gender,
            "events": root.events.ids,
            "images": root.images.ids,
            "sources": root.sources.ids,
            "children": [self._get_family_member(child) for child in root.children],
            # "mother": self._get_family_member(root.mother),
            # "father": self._get_family_member(root.father),
            # "siblings": [self._get_family_member(sibling) for sibling in root.siblings],
            # "spouses": [self._get_family_member(spouse) for spouse in root.spouses],
        }
    
    def _get_tree_data(self, tree):
        base = tree.ancestry_base
        return {
            "tree_name": tree.display_name,
            "family_name": tree.family_name,
            "client": base.client.name,
            "client_name": base.client.display_name,
            "count_audio": base.count_audio,
            "count_events": base.count_events,
            "count_people": base.count_people,
            "count_photos": base.count_photos,
            "count_records": base.count_records,
            "count_sources": base.count_sources,
            "count_stories": base.count_stories,
            "count_videos": base.count_videos,
            "invited_clients": base.invited_clients.ids,
            "members": self._get_family_member(tree.root_member),
        }