<%inherit file="/base.mako" />
<div style="width: 60%; float:left">

<%def name="pagetitle()">
Job Submission
</%def>

<H2> Cactus </H2>
<p> (Note that this service is only available for a user who has an account with LONI machines) </p>

<form name="cactus_input" method="POST" enctype="multipart/form-data" action="${url('/cactus/job_insert')}">

<table border="0"  cellspacing="0" cellpadding="5">
% for field in c.form:
%if field.is_hidden:
     ${field} 
%else:      

	   <tr>	
		<td> ${ field.label_tag() }   </td>
		<td> ${ field } </td>
		<td> ${ field.errors } </td>
	   </tr>
%endif
%endfor
</table>  

<input type="submit" name="Submit" value="Submit" />


</form>
</div>

<!--
<div style="width: 40%; float:right">
        <img src="${url('/workflow_Chipseq.png')}"  />
</div>
--!>