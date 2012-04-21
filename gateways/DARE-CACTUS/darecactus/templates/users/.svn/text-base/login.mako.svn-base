<%inherit file="/base.mako" />
	<br/>
	<br/>
${c.display_message}
<%def name="pagetitle()">
Job Submission
</%def>
<form name="user_login" method="POST" action="${url('/users/login_validate')}">

<table border="0"  cellspacing="0" cellpadding="5">


% for field in c.form:
%if field.is_hidden:
     ${field} 
%else:  

	   <tr>		
		<td> ${ field.label_tag() } </td>
		<td> ${ field } </td>
		<td> ${ field.errors } </td>
	   </tr>
%endif  
% endfor
</table>  

<input type="submit" name="login" value="Login" />

</form>
% if c.login=="invalid":
  Email and Password you have entered are invalid. Please enter valid email address and password or
<br />
%endif
If you have not registered yet, please <a href="${url('/users/register')}">click here</a> to register 
