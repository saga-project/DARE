
<%inherit file="/base.mako" />
<div style="width: 60%; float:left">
	<br/>
	<br/>

<%def name="pagetitle()">
Job Submission
</%def>

<H2> Genome-wide Mapping</H2>
The alignment of NGS short reads on to reference genome
is carried out with verious mapping tools

</br>
Figure on the right shows the schematic of a workflow with BFAST, one of mapping tools provided


<p>  Choose the mapping tool, the reference genome and sequenced data </p>
<p> (Note that this service is only available for a user who has an account with LONI machines) </p>
<form name="bfast_input" method="POST" enctype="multipart/form-data" action="${url('/ngs/job_insert')}">

<table border="0"  cellspacing="0" cellpadding="5">

% for field in c.form:

%if field.is_hidden:
     ${field}
%else:

	   <tr>
		<td > ${ field.label_tag() }   </td>
		<td > ${ field } </td>
		<td> ${ field.errors } </td>
	   </tr>
%endif

% endfor
</table>
<input type="submit" name="Submit" value="Submit" onclick="return checkform()" />
</form>
</div>

<div style="width: 40%; float:right">
        <img src="${url('/workflow_BFAST.png')}"  />
</div>
