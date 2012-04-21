<%inherit file="/base.mako" />
    <H2 align="justify"><br />
      <font color='#00007A'> DARE-NGS </font> <br />
     </H2>

<ul>

<li><H4>How CHiP-Seq is carried out?</H4>
<ul>
<li>Breaking the Fastq into small files</li>
<li>Transferring the multiple small files to distributed resources for processing (Assuming the Resources allready have reference genome) </li>
<li>Launching optimum size of resources</li>
<li>Carrying out all the steps till the Wig files are generated through Peak Calling</li>
</ul>
</li>

<li><H4>Input DATA:</H4>
<p>
Will be provided by the user prior to submitting a job
</p>

</li>

<li><H4>Features</H4>
<ul>
<li>Distributed  Computing</li>
<li>Choose tool for mapping (BWA/BFAST/BOWTIE)</li>
<li>Choose tool for Peak Calling (MACS/PEAKSEQ)</li>
</ul>


</li>
<li><H4>Advantages</H4>
<p>
Usability and Scalability along with faster results due to Distributed  Computing
</p>
</li>
<ul>