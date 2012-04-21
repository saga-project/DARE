<%inherit file="/base.mako" />
	<br/>
	<br/>

<%def name="pagetitle()">
Job Submission
</%def>



${h.form(url('job_update', id= c.jobs.jobid), method='Post')}

<table border="0"  cellspacing="0" cellpadding="5">
% for field in c.form:
	   <tr>		
		<td> ${ field.label_tag() }   </td>
		<td> ${ field } </td>
		<td> ${ field.errors } </td>
	   </tr>  
% endfor
</table>  

<input type="submit" name="submit" value="Submit" />

</form>

${c.mess}
