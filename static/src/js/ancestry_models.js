odoo.define('ancestry.family_tree', function (require) {
    "use strict";

    var AbstractModel = require('web.AbstractModel');

    var FamilyTreeModel = AbstractModel.extend({
        init: function () {
            this._super.apply(this, arguments);
            this.data = [];
        },

        // Load family tree data
        load: function (params) {
            var self = this;
            return this._rpc({
                model: 'ancestry.family_member',
                method: 'search_read',
                args: [],
                kwargs: {},
            }).then(function (result) {
                self.data = result;
            });
        },
    });

    return FamilyTreeModel;
});