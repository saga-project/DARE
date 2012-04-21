# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1328843225.289857
_template_filename='/Users/Sharath/workspace/projects/DARE-CACTUS/darecactus/templates/pages/job_table_view.mako'
_template_uri='/pages/job_table_view.mako'
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
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n<br/>\n<br/>\n')
        # SOURCE LINE 6
        __M_writer(u'\n\n')
        # SOURCE LINE 8
        __M_writer(escape(c.display_message))
        __M_writer(u'\n\n<h2> Submitted Jobs    </h2>\n\n    <!-- Jobs stored in the Database are shown here -->\n    <table border="0"  cellspacing="0" cellpadding="5">\n    <tr>\n    <th>Job ID</th>\n    <th>Description</th>\n    <th>App-Type</th>\n    <th>Status</th>\n   \n    <th>Submitted-Time</th>\n    <th>Actions</th>\n    </tr>\n\n')
        # SOURCE LINE 24
        for job in c.jobs:
            # SOURCE LINE 25
            if job.status == str(1): 
                # SOURCE LINE 26
                __M_writer(u'\t           <tr  bgcolor="#FFFFEE" >\n')
                # SOURCE LINE 27
            elif job.status == str(2) :
                # SOURCE LINE 28
                __M_writer(u'  \t         <tr  bgcolor="#EEFFEE" >  \n')
                # SOURCE LINE 29
            elif job.status == str(3):
                # SOURCE LINE 30
                __M_writer(u'  \t         <tr  bgcolor="#EECCEE" >  \n')
                # SOURCE LINE 31
            else:
                # SOURCE LINE 32
                __M_writer(u'  \t         <tr  bgcolor="white" >  \n')
                pass
            # SOURCE LINE 34
            __M_writer(u'\t\n            <td > ')
            # SOURCE LINE 35
            __M_writer(escape(job.id))
            __M_writer(u'  </td>\n            <td > \n')
            # SOURCE LINE 37
            for i in job.jobinfo:
                # SOURCE LINE 38
                if (i.key == "description"):           
                    # SOURCE LINE 39
                    __M_writer(u'                 ')
                    __M_writer(escape(i.value))
                    __M_writer(u'\n')
                    pass
                pass
            # SOURCE LINE 42
            __M_writer(u'            </td>\n            <td ><span style="text-transform: uppercase">             \n            \n')
            # SOURCE LINE 45
            for i in job.jobinfo:
                # SOURCE LINE 46
                if (i.key == "appname"):           
                    # SOURCE LINE 47
                    __M_writer(u'                 ')
                    __M_writer(escape(i.value))
                    __M_writer(u'\n')
                    pass
                pass
            # SOURCE LINE 50
            __M_writer(u'            \n            <td >   \n')
            # SOURCE LINE 52
            if job.status == str(1): 
                # SOURCE LINE 53
                __M_writer(u'\t               NEW\n')
                # SOURCE LINE 54
            elif job.status == str(2) :
                # SOURCE LINE 55
                __M_writer(u'  \t             RUNNING, ')
                __M_writer(escape(job.detail_status))
                __M_writer(u'   \n')
                # SOURCE LINE 56
            elif job.status == str(3):
                # SOURCE LINE 57
                __M_writer(u'  \t         FAILED, ')
                __M_writer(escape(job.detail_status))
                __M_writer(u' \n')
                # SOURCE LINE 58
            else: 
                # SOURCE LINE 59
                __M_writer(u'            \tDONE ')
                __M_writer(escape(job.detail_status))
                __M_writer(u'\n')
                pass
            # SOURCE LINE 61
            __M_writer(u'       \t\t\n       \t\t</td>\n            <td width="10%" > ')
            # SOURCE LINE 63
            __M_writer(escape(job.submitted_time))
            __M_writer(u' </td>\n\t    <td width="25%"><font size=\'2\'>\n\t\n\t')
            # SOURCE LINE 66
            __M_writer(escape(h.link_to("View Thorn", url('/cactus/download_job_input', jobid=job.id, type='thorn' ))))
            __M_writer(u'</br>\n\t')
            # SOURCE LINE 67
            __M_writer(escape(h.link_to("View Parameter file", url('/cactus/download_job_input', jobid=job.id, type='param' ))))
            __M_writer(u'</br>\n\t\n')
            # SOURCE LINE 69
            if job.status == str(1) or job.status == str(2)  : 
                # SOURCE LINE 70
                __M_writer(u'\t       ')
                __M_writer(escape(h.link_to("Update Status", url('/cactus/job_status_update', id=job.id))))
                __M_writer(u'<br/>\n')
                # SOURCE LINE 71
            else:
                # SOURCE LINE 72
                __M_writer(u'               ')
                __M_writer(escape(h.link_to("View Output", url('/cactus/download_job_output', jobid=job.id))))
                __M_writer(u'   <br/>\n')
                pass
            # SOURCE LINE 74
            __M_writer(u'        \n        ')
            # SOURCE LINE 75
            __M_writer(escape(h.link_to("Delete this Job", url('/cactus/job_delete', id=job.id))))
            __M_writer(u'\t\n\n\n          <br/>\n         <br/> \n         \n</font>\n\n  \t    </td>\n        </tr>\n')
            pass
        # SOURCE LINE 86
        __M_writer(u'    </table>\n\n')
        # SOURCE LINE 88
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


