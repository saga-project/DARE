# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1325559104.984416
_template_filename='/Users/Sharath/projects/projects_sw/DARE-CACTUS/darecactus/templates/forms/thorn_form.mako'
_template_uri='/forms/thorn_form.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from markupsafe import escape
_exports = ['pagetitle']


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
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n<div style="width: 60%; float:left">\n\n')
        # SOURCE LINE 6
        __M_writer(u'\n\n<H2> Cactus </H2>\n<p> (Note that this service is only available for a user who has an account with LONI machines) </p>\n\n<form name="thorn_input" method="POST" enctype="multipart/form-data" action="')
        # SOURCE LINE 11
        __M_writer(escape(url('/cactus/save_thorn')))
        __M_writer(u'">\n\n<table border="0"  cellspacing="0" cellpadding="5">\n')
        # SOURCE LINE 14
        for field in c.form:
            # SOURCE LINE 15
            if field.is_hidden:
                # SOURCE LINE 16
                __M_writer(u'     ')
                __M_writer(escape(field))
                __M_writer(u' \n')
                # SOURCE LINE 17
            else:      
                # SOURCE LINE 18
                __M_writer(u'\n\t   <tr>\t\n\t\t<td> ')
                # SOURCE LINE 20
                __M_writer(escape( field.label_tag() ))
                __M_writer(u'   </td>\n\t\t<td> ')
                # SOURCE LINE 21
                __M_writer(escape( field ))
                __M_writer(u' </td>\n\t\t<td> ')
                # SOURCE LINE 22
                __M_writer(escape( field.errors ))
                __M_writer(u' </td>\n\t   </tr>\n')
                pass
            pass
        # SOURCE LINE 26
        __M_writer(u'</table>  \n\n<input type="submit" name="Submit" value="Submit" />\n\n\n</form>\n</div>\n\n<!--\n<div style="width: 40%; float:right">\n        <img src="')
        # SOURCE LINE 36
        __M_writer(escape(url('/workflow_Chipseq.png')))
        __M_writer(u'"  />\n</div>\n--!>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_pagetitle(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\nJob Submission\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


