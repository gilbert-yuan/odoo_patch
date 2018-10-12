# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'odoo_patch',
    'version' : '1.1',
    'author': 'gilbert(静静yuan_wen_pu@163.com)',
    'summary': """
    可以配置edit create delete等参数实现动态（根据每条记录）的显示删除，新建、编辑按钮
        edit='{"color_domain": "state!=\"draft\""}'
        为啥叫color_domain 呢？因为最开始发现这种写法是在8上面的color的写法，是这样的。从这个上面获取的灵感。
         """,
    'sequence': 15,
    'category': 'tools',
    'depends': ['base'],
    'data': ["xml/odoo_patch.xml"],
    'installable': True,
    'application': True,
    'auto_install': False,
}
