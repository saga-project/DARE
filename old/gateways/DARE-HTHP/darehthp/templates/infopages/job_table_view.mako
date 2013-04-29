<%inherit file="/base.mako" />
<br/>
<br/>
<%def name="pagetitle()">
Submitted Jobs
</%def>
${c.display_message}
<h1> Job Information   </h1>
    <!-- Jobs stored in the Database are shown here -->
    <table border="0"  cellspacing="0" cellpadding="5">
    <tr>
    <th>Job ID</th>
    <th>Description</th>
    <th>App-Type</th>
    <th>Status</th>

    <th>Submitted-Time</th>
    <th>Actions</th>
    </tr>

    % for job in c.jobs:
       % if job.status == "New":
	   <tr  bgcolor="Yellow" >
       % elif job.status == "Running" :
  	   <tr  bgcolor="Red" >
       % elif job.status == "Failed":
  	   <tr  bgcolor="Green" >
       % else:
  	   <tr  bgcolor="white" >
       %endif
            <td > ${job.id}  </td>
            <td > ${job.description} </td>
            <td ><span style="text-transform: uppercase">  ${job.appname} </span> </td>
            <td > ${job.status}  </td>

            <td width="10%" > ${job.submitted_time} </td>
	    <td width="25%"><font size='2'>
	% if job.status == "New" or job.status == "Running"  :
		    ${h.link_to("Update this Job Status", url("/gateways/hthp/job_status_update", id=job.id))}
          <br/>
 % elif job.status=="Done":
       ${h.link_to("Download Output File", url("/gateways/hthp/output_download", id=job.id))}
         <br/>
 % endif
                ${h.link_to("Delete this Job", url("/gateways/hthp/job_delete", id=job.id))}
         <br/>

</font>

  	    </td>
        </tr>
    % endfor
    </table>

${c.pagenums}
