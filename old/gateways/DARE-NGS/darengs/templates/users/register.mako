<%inherit file="/base.mako" />
	<br/>
	<br/>
${c.display_message}

<%def name="pagetitle()">
Job Submission
</%def>
<form name="user_login" method="POST" action="${url('/users/register_post')}">

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
% if c.email == "invalid":
 <p>Given email already exists. Please use a different email</p>
% endif
