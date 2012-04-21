# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1324141310.854068
_template_filename='/Users/Sharath/projects/projects_sw/DARE-CACTUS/darecactus/templates/users/succ_register.mako'
_template_uri='/users/succ_register.mako'
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
        url = context.get('url', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\t<br/>\n<br/>\n\nsuccessfully registered please click <a href="')
        # SOURCE LINE 5
        __M_writer(escape(url('/users/login')))
        __M_writer(u'">here</a> to login\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


