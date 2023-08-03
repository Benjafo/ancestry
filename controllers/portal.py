from odoo import api, fields, models, route
from odoo.addons.portal.controllers import portal

class AncestryPortal(portal.CustomerPortal):

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        res = super().home()