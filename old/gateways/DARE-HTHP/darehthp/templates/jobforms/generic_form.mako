<%inherit file="/base.mako" />

Job >> Define Resources >> Define Tasks(Work Units) >> Submit Job

	<br/>
	<br/>


<%def name="pagetitle()">
Job Submission
</%def>
Job Submission

<form id="genform" name="namd_input" method="POST" enctype="multipart/form-data" action="${url('/hthpmd/job_insert')}">
<input value="0" name="numfiles" id="id_numfiles" type="hidden">
<input value="1" name="numresources" id="id_numresources" type="hidden">
<table id ="tablea"border="0"  cellspacing="0" cellpadding="5">

% for field in c.form:

%if field.is_hidden:
     ${field}
%else:

	   <tr>
		<td> ${ field.label_tag() } *  </td>
		<td> ${ field } </td>
		<td> ${ field.errors } </td>
	   </tr>
%endif

% endfor


</table>

<!--<p><a href="javascript:;" onclick="addresource();">Add New Resource</a></p>


<p><a href="javascript:;" onclick="addElement();">Add New file</a></p>

--!>
<input type="submit" name="Submit" value="Submit" onclick="return checkform()" />
<p> * Indicates Mandatory form fields </a></p>


</form>
<script type="text/javascript">

  function addElement() {

  var numi = document.getElementById('id_numfiles');
  var num = (document.getElementById('id_numfiles').value -1)+ 2;
  numi.value = num;
  var newfile = document.createElement('input');
  var fileIdName = 'file'+num;
  var myTable = document.getElementById('tablea');
  var tBody = myTable.getElementsByTagName('tbody')[0];
  var newTR = document.createElement('tr');
  newTR.setAttribute('id','tr'+fileIdName);
  var newTD = document.createElement('td');
  var newTDl = document.createElement('td');
  var newTDt = document.createElement('td');
  newfile.setAttribute('type','file');
  newfile.setAttribute('id',fileIdName);
  newfile.setAttribute('name',fileIdName);
  newTDl.innerHTML = 'Input file ' + num;
  newTD.appendChild(newfile)
  newTR.appendChild (newTDl);
  newTR.appendChild (newTD);
  newTR.appendChild (newTDt);
  tBody.appendChild(newTR);

}

  function addresource() {



  var numi = document.getElementById('id_numresources');
  var num = (document.getElementById('id_numresources').value -1)+ 2;
  numi.value = num;
  var myTable = document.getElementById('tablea');
  var tBody = myTable.getElementsByTagName('tbody')[0];


  var mylists = document.getElementById('id_choose_machine');
  //var mylist =  document.createElement('option');
  var mylist = mylists.cloneNode(true);

  var newtextm = document.createElement('input');

  var fileIdNamem = 'resourcename'+num;

  var newTRm = document.createElement('tr');
  var newTDm = document.createElement('td');
  var newTDmd = document.createElement('td');

  newTRm.setAttribute('id','tr'+fileIdNamem);
  mylist.setAttribute('id',fileIdNamem);
  mylist.setAttribute('name',fileIdNamem);


  newTDmd.innerHTML = 'Resource ' + num + ' machine ';
  newTDm.appendChild(mylist);

  newTRm.appendChild (newTDmd);
  newTRm.appendChild (newTDm);
  tBody.appendChild(newTRm);





  var newtexts = document.createElement('input');

  var fileIdNames = 'resourcejob'+num;


  var newTRs = document.createElement('tr');

  newTRs.setAttribute('id','tr'+fileIdNames);

  var newTDs = document.createElement('td');
  var newTDsd = document.createElement('td');

  newtexts.setAttribute('type','text');
  newtexts.setAttribute('id',fileIdNames);
  newtexts.setAttribute('name',fileIdNames);

  newTDsd.innerHTML = 'Resource ' + num + ' NAMD Size';
  newTDs.appendChild(newtexts);
  newTRs.appendChild (newTDsd);
  newTRs.appendChild (newTDs);
  tBody.appendChild(newTRs);


  var fileIdNamen = 'resourcesize'+num;
  var newtextn = document.createElement('input');

  var newTRn = document.createElement('tr');
  var newTDn = document.createElement('td');
  var newTDnd = document.createElement('td');

  newTRn.setAttribute('id','tr'+fileIdNamen);
  newtextn.setAttribute('type','text');
  newtextn.setAttribute('id',fileIdNamen);
  newtextn.setAttribute('name',fileIdNamen);

  newTDnd.innerHTML = 'Resource ' + num + ' num of NAMD jobs';
  newTDn.appendChild(newtextn);

  newTRn.appendChild (newTDnd);
  newTRn.appendChild (newTDn) ;

  tBody.appendChild(newTRn);

}


  function removeElement(divNum) {
  var numi = document.getElementById('numfiles');
  var num = (document.getElementById('numfiles').value -1);
  numi.value = num;
  var fileIdName = 'file'+num;
  var myTable = document.getElementById('tablea');
  var tBody = myTable.getElementsByTagName('tbody')[0];
  tBody.removeChild(divNum);

}



</script>

