<%inherit file="/base.mako" />
    <H2 align="justify"><br />
      <font color='#00007A'> Dalliance </font> <br />
      <span class="twoColHybRtHdr">
      </H2>
      
      
<script language="javascript" src="http://www.biodalliance.org/js/dalliance-compiled.js"></script>

<script language="javascript">
  new Browser({
    chr:          '22',
    viewStart:    30000000,
    viewEnd:      30030000,
    cookieKey:    'human',

    sources:     [{name:                 'Genome',      
                   uri:                  'http://www.derkholm.net:8080/das/hg18comp/',        
                   tier_type:            'sequence',
                   provides_entrypoints: true},
                  {name:                 'Genes',     
                   desc:                 'Gene structures from Ensembl 54',
                   uri:                  'http://www.derkholm.net:8080/das/hsa_54_36p/',      
                   collapseSuperGroups:  true,
                   provides_karyotype:   true,
                   provides_search:      true},
                  {name:                 'Repeats',     
                   uri:                  'http://www.derkholm.net:8080/das/hsa_54_36p/',      
                   stylesheet_uri:       'http://www.derkholm.net/dalliance-test/stylesheets/ens-repeats.xml'},
                  {name:                 'MeDIP raw',
                   uri:                  'http://www.derkholm.net:8080/das/medipseq_reads'},
                  {name:                 'MeDIP-seq',
                   uri:                  'http://www.ebi.ac.uk/das-srv/genomicdas/das/batman_seq_SP/'}],

    searchEndpoint: new DASSource('http://www.derkholm.net:8080/das/hsa_54_36p/'),
    browserLinks: {
    
    <%text>
        Ensembl: 'http://ncbi36.ensembl.org/Homo_sapiens/Location/View?r=${chr}:${start}-${end}',
        UCSC: 'http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg18&position=chr${chr}:${start}-${end}',
        </%text>
    },

    forceWidth: 700
  });
</script>

<div id="svgHolder"> </div>




