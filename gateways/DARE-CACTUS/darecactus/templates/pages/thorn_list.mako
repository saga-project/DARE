<%inherit file="/base.mako" />
<br/>
<br/>
<%def name="pagetitle()">
Submitted Jobs
</%def>

${c.display_message}

<h2> Available Thorns    </h2>

    <!-- Jobs stored in the Database are shown here -->
    <table border="0"  cellspacing="0" cellpadding="5">
    <tr>
    <th>Thorn-File</th>
    <th>Description</th>
    <!--  <th>Available machines</th> -->   
   
    <th>Submitted-Time</th>
    <th>Actions</th>
    </tr>
<!--#todo if c. form not empty--!>
    % for thorn in c.thornlist:
	    <tr>
            <td> ${thorn.filename}  </td>
            <td> ${thorn.description}</td>
            <td> ${thorn.submitted_time}</td>
            <td> 
            ${h.link_to("View Thorn", url('/cactus/download_thorn', id=thorn.id ))}
        </tr>



    % endfor
    </table>
    
 <a href='${url('/cactus/upload_thorn')}'>Upload Thorn</a>   

${c.pagenums}
