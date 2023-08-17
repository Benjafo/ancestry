odoo.define('ancestry.FamilyTreeView', function (require) {
    "use strict";

    var AbstractView = require('web.AbstractView');
    var viewRegistry = require('web.view_registry');

    var FamilyTreeView = AbstractView.extend({
        display_name: "Family Tree",
        icon: 'fa-sitemap',
        config: _.extend({}, AbstractView.prototype.config, {
            Model: 'ancestry.family_tree',
            Renderer: 'ancestry.FamilyTreeRenderer',
        }),
    });

    viewRegistry.add('family_tree', FamilyTreeView);

    return FamilyTreeView;
});