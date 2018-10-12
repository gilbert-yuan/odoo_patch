odoo.define('odoo.patch', function(require) {
"use strict";

var FormController = require('web.FormController');

 FormController.include({
    is_action_enabled: function (action) {
        if (['true', 'false', '0', '1'].indexOf(this.activeActions[action]) < 0 && this.activeActions[action].color_domain){
            return JSON.parse(py.evaluate(py.parse(py.tokenize(this.activeActions[action].color_domain)), this.initialState.data).toJSON());
        }else {
             return this.activeActions[action]
        }
    },
 });

});