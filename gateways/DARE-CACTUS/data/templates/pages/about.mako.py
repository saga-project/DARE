# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1325530820.227767
_template_filename='/Users/Sharath/projects/projects_sw/DARE-CACTUS/darecactus/templates/pages/about.mako'
_template_uri='/pages/about.mako'
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
        __M_writer(u'\n    <H2 align="justify"><br />\n      <font color=\'#00007A\'> DARE-CACTUS </font> <br />\n      <span class="twoColHybRtHdr">\n      </H2>\n<p>\nDARE-CACTUS is a Gateway for Cactus based applications which builds upon the Dynamic Application Runtime-Environment (DARE) Framework.\n</p>\n\n\nAt the moment, there are no general-purpose community accounts, and it requires registrations contacting us before using services. \nFor more information, contact us. For information about SAGA and SAGA-Bigjob, please visit this link\n<a href="http://saga.cct.lsu.edu/">link</a></font></p>\n    </p>\n    <table width="725" border="0">\n      <tr>\n        <td width="332"><img src="')
        # SOURCE LINE 17
        __M_writer(escape(url('/DAREOutline.png')))
        __M_writer(u'" width="500" height="420" alt="DARE" /></td>\n      </tr>\n      <tr>\n        <td><span style=" font-size:11px">Dynamic Application Runtime Environment(DARE)</span></td>\n      </tr>\n    </table>\n    <p><br class="clearfloat" />\n    </p>\n\n\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


