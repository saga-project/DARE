<%inherit file="/base.mako" />
<br/>
<br/>
<%def name="pagetitle()">
Submitted Jobs
</%def>

${c.display_message}

<h2> Submitted Jobs    </h2>

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
       % if job.status == str(1): 
	           <tr  bgcolor="Yellow" >
       % elif job.status == str(2) :
  	         <tr  bgcolor="Green" >  
       % elif job.status == str(3):
  	         <tr  bgcolor="Red" >  
       % else:
  	         <tr  bgcolor="white" >  
       %endif
	
            <td > ${job.id}  </td>
            <td > 
            % for i in job.jobinfo:
             %   if (i.key == "description"):           
                 ${i.value}
            % endif
            % endfor
            </td>
            <td ><span style="text-transform: uppercase">             
            
            % for i in job.jobinfo:
             %   if (i.key == "appname"):           
                 ${i.value}
            % endif
            % endfor </span> </td>
            
            <td >   
            % if job.status == str(1): 
	               NEW
       		% elif job.status == str(2) :
  	             RUNNING, ${job.detail_status}   
      	 	% elif job.status == str(3):
  	         FAILED, ${job.detail_status} 
       		% else: 
            	DONE ${job.detail_status}
       		%endif
       		
       		</td>
            <td width="10%" > ${job.submitted_time} </td>
	    <td width="25%"><font size='2'>
	% if job.status == str(1) or job.status == str(2)  : 
		    ${h.link_to("Update this Job Status", url('/ngs/job_status_update', id=job.id))}
          <br/>
 %else:
               % for i in job.jobinfo:
                 % if (i.key == "appname"):  
                     %   if (i.value =="tophat"):
                 		    ${h.link_to("View Output", url('/ngs/tophatfusion_view', id=job.id))}
                 		     <br/>
                     % endif               
                 % endif
              % endfor

	 % endif	
                ${h.link_to("Delete this Job", url('/ngs/job_delete', id=job.id))}	


          <br/>
         <br/> 
         
</font>

  	    </td>
        </tr>
    % endfor
    </table>

${c.pagenums}
