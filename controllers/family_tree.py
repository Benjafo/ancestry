from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal

class AncestryFamilyTree(CustomerPortal):

    @route('/my/tree', type='http', auth="public", website=True)
    def tree(self, **kwargs):
        values = self._prepare_portal_layout_values()
        values.update({
            'ancestry': request.env['ancestry.tree'].sudo().search([('ancestry_base.id', '=', request.env.user.commercial_partner_id.id)]),
        })
        return request.render("ancestry.portal_ancestry_record", values)
