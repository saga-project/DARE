<%inherit file="/base.mako" />\
	<br/>
	<br/>

your job successfully submitted. 

	
	<FORM  name="goto_jobtable" method="GET"  action="/job_table_view"
>
	
	<input type="submit" name="Go to the Job List Table" value="See Job Table">

	
	</FORM>


	
	<FORM name="goto_jobsubmit" method="GET" action="/job_submit">
	
	<input type="submit" name="Go to the page for another job submission" value="Submit another job">

	
	</FORM>



