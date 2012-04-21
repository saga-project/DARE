# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1333596249.352634
_template_filename='/Users/Sharath/workspace/projects/DARE-CACTUS/darecactus/templates/pages/using_cactus.mako'
_template_uri='/pages/using_cactus.mako'
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
        __M_writer(u'\n    <H2 align="justify"><br />\n      <font color=\'#00007A\'> DARE-CACTUS </font> <br />\n     </H2>\n<ul>\n<li><H4>How cactus is carried out?</H4>\n<p>\n<ul>\n\n<li>Launching optimum size of resources</li>\n\n</ul>\n</p>\n</li>\n<li><H4>Input DATA:</H4>\n<p>\nWill be provided by the user while submitting a job(thorn file, parameter file)\n</p>\n</li>\n\n<li><H4>Features</H4>\n<p>\nDistributed  Computing\n</p>\n\n</li>\n\n<li>\n\t<H4>Steps</H4>\n\t<H5>Stage-1</H5>\t\n\t\t<b>Step-1:</b> Create DARE working directories and cactus build directories<br/>\n\t\t<b>Step-2:</b> Transfer thorn-file and parameter-file to remote machine<br/>\n\t\t<b>Step-3:</b> Downnload Getcomponents via WGET<br/>\n\t\t<b>Step-4:</b> Run Getcomponents with the given thornfile <br/>\n\t\t<b>Step-5:</b> Now transfer the cactus_installer.py file ("cactus_installer.py" checks for the executable \'cactus_sim\' exists or not and builds cactus if necessary.)<br/>\n\t\t<b>Step-6:</b> run cactus_installer.py to actually build cactus with downloded thorns if necessary.<br/>\n\n\t<H5>Stage-2</H5>\t                  \n\t\t<b>Step-1(7):</b> Create cactus simulation directory<br/>\n\t\t<b>Step-2(8):</b> Run cactus simulation through cactus mpi and given parameter file<br/>\n\t\t<b>Step-3(9):</b> Tar the output parameter file<br/>\n\t\t<b>Step-4(10):</b>Transfer the output file back to this server. <br/>\n\n\t\n</li>\n\n\n\n\n<li>\n\t<H4>Advantages</H4>\n\t<p>\n\t\tUsability and Scalability along with faster results due to Distributed Computing\n\t</p>\n</li>\n\n</ul>\n\n\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


