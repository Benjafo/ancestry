from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request, route

class AncestryPortal(CustomerPortal):

    @route('/my/ancestry', type='http', auth="user", website=True)
    def ancestry(self, **kwargs):
        values = super()._prepare_portal_layout_values()
        values.update({
            'ancestry': request.env['ancestry.ancestry'].sudo().search([('client.id', '=', request.env.user.commercial_partner_id.id)])
        })
        return request.render("ancestry.portal_my_ancestry", values)
