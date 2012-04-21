# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1328843921.978473
_template_filename='/Users/Sharath/workspace/projects/DARE-CACTUS/darecactus/templates/pages/contact.mako'
_template_uri='/pages/contact.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from markupsafe import escape
_exports = []


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n<p> \nThis project is being developed by Cyber-Infrastructure Develop (CyD) Group at Center for Computational Technology(CCT)</p>\n \n <p>\n\n<b>Project Lead:</b><br />\n      Dr. Shantenu Jha (<a href="mailto:sjha@cct.lsu.edu">sjha@cct.lsu.edu</a>)\n\n</p>\n\n\n\n\n<div>\n<b>Team:</b> <br />\n<div>\n       Steve Brandt (<a href="mailto:sbrandt@cct.lsu.edu">sbrandt@cct.lsu.edu</a>)\n</div>\n<div> \n      Ole  Weidner (<a href="mailto:oweidner@cct.lsu.edu">oweidner@cct.lsu.edu</a>)\n</div>\n<div>\n       Sharath Maddineni (<a href="mailto:smaddineni@cct.lsu.edu">smaddineni@cct.lsu.edu</a>)\n</div>\n</div>\n\n<p>\n<b>\nFunding:\n</b>  \n<a href=\'https://sites.google.com/site/extenci/\' >ExTENCI</a>\n<br />\n</p>')
        return ''
    finally:
        context.caller_stack._pop_frame()


