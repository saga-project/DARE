<%inherit file="/base.mako" />
<div style="width: 60%; float:left">
<%def name="pagetitle()">
Job Submission
</%def>

<H2> TOPHAT-FUSION </H2>
<p> Figure on the right shows the Pipeline and Tools used</p>
<p>  Fill the following form and click Submit button. This service requires a reference genome and sequenced reads data uploaded.  For more details, please contact us.</p>

<form name="tophat_input" method="POST" enctype="multipart/form-data" action="${url('/ngs/job_insert')}">

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
% endfor
</table>  

<input type="submit" name="Submit" value="Submit" onclick="return checkform()" />

</form>
</div>

<div style="width: 40%; float:right">
        <img src="${url('/workflow_TOPHAT.png')}"  />
</div>

