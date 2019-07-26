# odoo_patch
## TO-DO-LIST
- [X] 可以配置  form 的参数 edit create delete等， 实现动态（根据每条记录）的显示删除、新建、编辑等按钮
         domain 表示方式 edit='{"color_domain": "state!=\\"draft\\""}'
 
 ### 下面几个带详细代码的都是项目中遇到的问题，只是在odoo 10 中的解决方案。稍后测试看是否12中也有，然后进行升级
- [ ]  odoo 中 Many2one搜索更多时搜索不出想要的结果 只能搜索出前160条中满足条件记录数（10.0中发现的以后版本有没有这个问题还未测试）
```js
    var form_common = require('web.form_common');
    form_common.SelectCreateDialog.include({
        setup: function () {
            this.initial_ids = undefined;
            return this._super.apply(this, arguments);
        }
    });
```
-[ ] odoo中radio 不可以横向排列，看配置项是可以的看了js才发现有BUG
```js
     var include_radio = core.form_widget_registry.get('radio');
     include_radio.include({
        initialize_content: function() {
            this._super();
            if (this.options.hesai_horizontal) {
                this.$el.removeClass('o_form_field');
            }
        },
    });   
```
-[ ] odoo中点击button直接下载文件解决方案（仅限于小文件，大文件等待时间过长不适合这种方式）
曾经尝试的方案- return一个action target 为new 会被系统拦截，return一个action target 为self 这个按钮只能点击一次 。
所以费劲心思想出这个方案。
```python 
   button_html = fields.Char(compute="_compute_button_html",
                              string='Create Excel')

    @api.depends('start_date', 'end_date')
    def _compute_button_html(self):
        for wizard in self:
            wizard.button_html = _("""<a href="/employee/export/attendance_excel/%s/%s/%s" 
                class="btn btn-sm oe_highlight">Download Excel</a>"""
                                   ) % (wizard.start_date, wizard.end_date, wizard.emp_id.id)
```

```xml
<field name="button_html" widget="down_load_file"   attrs="{'invisible':[('id', '=', False)]}"
                              string="Create Excel"/>
```
```js
   var ButtonDownloadFiled = form_common.AbstractField.extend({
        init: function (parent, object) {
            this._super.apply(this, arguments);
        },
        render_value: function () {
            var self = this;
            self.$el.html(self.get_value());
            return self._super();
        },

    });
    core.form_widget_registry.add('down_load_file', ButtonDownloadFiled);
```
-[ ] odoo 中扫码的场景， 运用onchange 可以完美解决单个输入框的问题， 可是既要输入号码，又要输入数量的场景下就很难处理
下面场景中需要配合onchange，在onchange中加入字段对应表中加入字段并需要跳到下一个输入框时，onchange中self.autofocus = True

```js

FormView.include({
        on_processed_onchange: function (result) {
            var return_val = this._super.apply(this, arguments);
            if (result.value && result.value.autofocus) {
                this.autofocus()
            }
            return return_val
        },
        autofocus: function() {
            if (this.get("actual_mode") !== "view" && !this.options.disable_autofocus) {
                var fields_order = this.fields_order.slice(0);
                if (this.default_focus_field) {
                    fields_order.unshift(this.default_focus_field.name);
                }
                for (var i = 0; i < fields_order.length; i += 1) {
                    var field = this.fields[fields_order[i]];
                    if (!field.get('effective_invisible') && !field.get('effective_readonly') && field.$label) {
                        if (field.focus() !== false) {
                            if(field.node && field.node.attrs &&field.node.attrs.position== "{'not_none_focus': True}" && field.get_value()) {
                                continue
                            }
                            break;
                        }
                    }
                }
            }
        },
    });

```

-[ ] odoo 一个列表翻到了第3页需要查看一条的详细内容，点进去查看编辑form 返回tree 视图，然后直接跳到了第一页，one2many删除单行会跳到上一页，等翻页问题解决，
```js
 ListView.Groups.include({
        render_dataset: function () {
            this.view.current_min = this.view.pager && this.view.pager.state ? this.view.pager.state.current_min: 1;
            var return_val = this._super.apply(this, arguments);
            return return_val
        }
    });
    ListView.include({
        do_delete: function (ids) {
            if (!(ids.length && confirm(_t("Do you really want to remove these records?")))) {
                return;
            }
            var self = this;
            return $.when(this.dataset.unlink(ids)).done(function () {
                _(ids).each(function (id) {
                    self.records.remove(self.records.get(id));
                });
                // Hide the table if there is no more record in the dataset
                if (self.display_nocontent_helper()) {
                    self.no_result();
                } else {
                    if (self.records.length && self.current_min === 1) {
                        // Reload the list view if we delete all the records of the first page
                        self.reload();
                    } else if (self.records.length && self.dataset.size() < self.current_min) {
                        // Load previous page if the current one is empty
                        self.pager.previous();
                    }
                    // Reload the list view if we are not on the last page
                    if (self.current_min + self._limit - 1 < self.dataset.size()) {
                        self.reload();
                    }
                }
                self.update_pager(self.dataset);
                self.compute_aggregates();
            });
        },
    });

```





