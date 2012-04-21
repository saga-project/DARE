<%inherit file="/base.mako" />
	<br/>
	<br/>

<%def name="pagetitle()">
Job Submission
</%def>
NAMD Job Submission
<p> (Note that this service is only available for a user who has an account with LONI machines) </p>


<form id="namdform" name="namd_input" method="POST" enctype="multipart/form-data" action="${url('/hthpmd/namd_job_insert')}">

<table id ="tablea"border="0"  cellspacing="0" cellpadding="5">
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


<input type="submit" name="Submit" value="Submit" />

</form>

<SCRIPT LANGUAGE="javascript">
<!--
function OnChange(dropdown)
{
    document.forms["namdform"].action ="${url('/hthpmd/namd_form?action=newresource')}";

    document.forms["namdform"].submit();
    
    return true;
}
function OnChangef(dropdown)
{
    document.forms["namdform"].action ="${url('/hthpmd/namd_form?action=newresource')}";

    document.forms["namdform"].submit();
    
    return true;
}

//-->

</SCRIPT>

<!--var baseURL  = "${url('/hthpmd/namd_form')}"
if  field.label_tag().startswith('Resource'):
hggf

endif

    top.location.href = baseURL; --!>
    

