# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1328843234.305318
_template_filename='/Users/Sharath/workspace/projects/DARE-CACTUS/darecactus/templates/pages/software.mako'
_template_uri='/pages/software.mako'
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
        __M_writer(u'\n\t<br/>\n\t<br/>\n\nAll scripts are now under testing(beta), however  please contact <a href="mailto:smaddineni@cct.lsu.edu">  smaddineni@cct.lsu.edu </a> for information about the available scripts.')
        return ''
    finally:
        context.caller_stack._pop_frame()


