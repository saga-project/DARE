# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1325807700.124456
_template_filename='/Users/Sharath/projects/projects_sw/DARE-CACTUS/darecactus/templates/pages/thorn_list.mako'
_template_uri='/pages/thorn_list.mako'
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
        h = context.get('h', UNDEFINED)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n<br/>\n<br/>\n')
        # SOURCE LINE 6
        __M_writer(u'\n\n')
        # SOURCE LINE 8
        __M_writer(escape(c.display_message))
        __M_writer(u'\n\n<h2> Available Thorns    </h2>\n\n    <!-- Jobs stored in the Database are shown here -->\n    <table border="0"  cellspacing="0" cellpadding="5">\n    <tr>\n    <th>Thorn-File</th>\n    <th>Description</th>\n    <!--  <th>Available machines</th> -->   \n   \n    <th>Submitted-Time</th>\n    <th>Actions</th>\n    </tr>\n<!--#todo if c. form not empty--!>\n')
        # SOURCE LINE 23
        for thorn in c.thornlist:
            # SOURCE LINE 24
            __M_writer(u'\t    <tr>\n            <td> ')
            # SOURCE LINE 25
            __M_writer(escape(thorn.filename))
            __M_writer(u'  </td>\n            <td> ')
            # SOURCE LINE 26
            __M_writer(escape(thorn.description))
            __M_writer(u'</td>\n            <td> ')
            # SOURCE LINE 27
            __M_writer(escape(thorn.submitted_time))
            __M_writer(u'</td>\n            <td> \n            ')
            # SOURCE LINE 29
            __M_writer(escape(h.link_to("View Thorn", url('/cactus/download_thorn', id=thorn.id ))))
            __M_writer(u'\n        </tr>\n\n\n\n')
            pass
        # SOURCE LINE 35
        __M_writer(u"    </table>\n    \n <a href='")
        # SOURCE LINE 37
        __M_writer(escape(url('/cactus/upload_thorn')))
        __M_writer(u"'>Upload Thorn</a>   \n\n")
        # SOURCE LINE 39
        __M_writer(escape(c.pagenums))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_pagetitle(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\nSubmitted Jobs\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


