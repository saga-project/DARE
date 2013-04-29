# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1322434651.240422
_template_filename='/Users/Sharath/projects/projects/DARE-NGS/darengs/templates/pages/index.mako'
_template_uri='/pages/index.mako'
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
        __M_writer(u'\n    <H2 align="justify"><br />\n      <font color=\'#00007A\'> DARE-NGS </font> <br />\n      <span class="twoColHybRtHdr">\n      </H2>\n<p>\nDARE-NGS is a Gateway for Next Generation Sequence data analysis. DARE-NGS supports Genome-wide analysis --\nwhich is both computationally and data-intensive. DARE-NGS builds upon the Dynamic Application Runtime-Environment (DARE) Framework,\nand is one of several Science Gateways for Life Science Applications built using DARE.\n</p>\n<p>\nGateways enable non-experts to seamlessly utilize High-Performance and Distributed Computing resources, such as the NSF\'s national production cyberinfrastructure\n-- XSEDE, regional cyberinfrastructure resources such as LONI. DARE-based Gateways can be extended to utilize campus/departmental clusters too.\n</p>\n<p>\nCurrently, registered users who agree the data management policy can run BFast, Bowtie,\nand BWA for mapping, our ChIP-Seq pipeline, and Tophat-fusion for fusion gene discovery.\nMore tools are coming. Currently DARE-NGS uses LONI and TeraGrid resources for production\nand FutureGrid-Clouds for testing. DARE-NGS will be made available for a broad range of\nprivate and commercial Cloud Services in early 2012.\n</p>\n\nAt the moment, there are no general-purpose community accounts, and it requires registrations contacting us before using services.\nFor more information, contact us. For information about SAGA and SAGA-Bigjob, please visit this\n<a href="http://saga.cct.lsu.edu/">Link</a></font></p>\n    </p>\n\n    <p><br class="clearfloat" />\n    </p>\n\n\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


