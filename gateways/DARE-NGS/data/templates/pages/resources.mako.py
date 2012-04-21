# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1322434653.669653
_template_filename='/Users/Sharath/projects/projects/DARE-NGS/darengs/templates/pages/resources.mako'
_template_uri='/pages/resources.mako'
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
        __M_writer(u'\n \n\n   <table >\n      <tr>\n        <th >  Machine          </th>\n        <th >  Location          </th>\n        <th >  Info             </th>\n        <th >  Job Submission Type   </th>\n\n      </tr>\n\n      <tr>\n        <td > Cyder   </td>\n        <td > LSU/CCT  </td>\n        <td > 12 core, 5.2 TB HD  </td>\n        <td > SAGA/SSH   </td>\n      </tr>\n      <tr>\n        <td >  Queen Bee   </td>\n        <td > LONI  </td>\n        <td > 8 core/node, 512 Nodes   </td>\n        <td >  GLOBUS/SAGA   </td>\n      </tr>\n      <tr>\n        <td >  Ranger   </td>\n        <td >  TERAGRID  </td>\n        <td > 16 core/node,   </td>\n        <td >  GLOBUS/SAGA   </td>\n      </tr>\n\n\n\n    </table>\n\n\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


