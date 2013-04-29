# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1322434660.037926
_template_filename='/Users/Sharath/projects/projects/DARE-NGS/darengs/templates/dalliance.mako'
_template_uri='/dalliance.mako'
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
        __M_writer(u'\n    <H2 align="justify"><br />\n      <font color=\'#00007A\'> Dalliance </font> <br />\n      <span class="twoColHybRtHdr">\n      </H2>\n      \n      \n<script language="javascript" src="http://www.biodalliance.org/js/dalliance-compiled.js"></script>\n\n<script language="javascript">\n  new Browser({\n    chr:          \'22\',\n    viewStart:    30000000,\n    viewEnd:      30030000,\n    cookieKey:    \'human\',\n\n    sources:     [{name:                 \'Genome\',      \n                   uri:                  \'http://www.derkholm.net:8080/das/hg18comp/\',        \n                   tier_type:            \'sequence\',\n                   provides_entrypoints: true},\n                  {name:                 \'Genes\',     \n                   desc:                 \'Gene structures from Ensembl 54\',\n                   uri:                  \'http://www.derkholm.net:8080/das/hsa_54_36p/\',      \n                   collapseSuperGroups:  true,\n                   provides_karyotype:   true,\n                   provides_search:      true},\n                  {name:                 \'Repeats\',     \n                   uri:                  \'http://www.derkholm.net:8080/das/hsa_54_36p/\',      \n                   stylesheet_uri:       \'http://www.derkholm.net/dalliance-test/stylesheets/ens-repeats.xml\'},\n                  {name:                 \'MeDIP raw\',\n                   uri:                  \'http://www.derkholm.net:8080/das/medipseq_reads\'},\n                  {name:                 \'MeDIP-seq\',\n                   uri:                  \'http://www.ebi.ac.uk/das-srv/genomicdas/das/batman_seq_SP/\'}],\n\n    searchEndpoint: new DASSource(\'http://www.derkholm.net:8080/das/hsa_54_36p/\'),\n    browserLinks: {\n    \n    ')
        # SOURCE LINE 38
        __M_writer(u"\n        Ensembl: 'http://ncbi36.ensembl.org/Homo_sapiens/Location/View?r=${chr}:${start}-${end}',\n        UCSC: 'http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg18&position=chr${chr}:${start}-${end}',\n        ")
        # SOURCE LINE 41
        __M_writer(u'\n    },\n\n    forceWidth: 700\n  });\n</script>\n\n<div id="svgHolder"> </div>\n\n\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


