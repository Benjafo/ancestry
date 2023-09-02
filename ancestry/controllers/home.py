from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request, route

class AncestryPortal(CustomerPortal):

    @route('/my/home', type='http', auth="user", website=True)
    def home(self, **kwargs):
        #values = super()._prepare_portal_layout_values()
        values = ({#values.update({
            'ancestry_count': 3 #len(request.env['ancestry.ancestry'].sudo().search([('client.id', '=', request.env.user.commercial_partner_id.id)]).family_tree)
        })
        return request.render("ancestry.portal_my_ancestry", values)