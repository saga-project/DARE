from django.db import models
from django.contrib import admin


simple_task_script = """def tasks(NUMBER_JOBS=1):
    tasks = []
    for i in range(NUMBER_JOBS):
        compute_unit_description = {
        "executable": "/bin/echo",
        "arguments": ["Hello", "$ENV1", "$ENV2"],
        "environment": ['ENV1=env_arg1', 'ENV2=env_arg2'],
        "number_of_processes": 4,
        "spmd_variation": "mpi",
        "output": "stdout.txt",
        "error": "stderr.txt"}
        tasks.append(compute_unit_description)
    return tasks"""


class BaseDareModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30, null=False, blank=False, default='name')
    status = models.CharField(max_length=30, null=False, blank=False, default='New')
    user = models.ForeignKey('auth.User')

    class Meta:
        abstract = True

    def __unicode__(self):
        if self.name:
            return self.name
        return str(self.id)


class BaseDareBigJobPilot(BaseDareModel):
    pilot_type = models.CharField(max_length=10)
    service_url = models.CharField(max_length=256)
    data_service_url = models.CharField(max_length=256,  blank=True)
    working_directory = models.CharField(max_length=30, blank=True)
    cores_per_node = models.IntegerField(default=1)
    number_of_processes = models.IntegerField(default=1)
    queue = models.CharField(max_length=30, blank=True)
    project = models.CharField(max_length=30, blank=True)
    walltime = models.IntegerField(default=10)

    class Meta:
        abstract = True


class DefaultDareBigJobPilot(BaseDareBigJobPilot):
    pass


class DefaultDareBigJobPilotAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'service_url', 'cores_per_node', 'number_of_processes', 'queue', 'project', 'walltime')

admin.site.register(DefaultDareBigJobPilot, DefaultDareBigJobPilotAdmin)


class DareBigJob(BaseDareModel):
    cordination_url = models.CharField(max_length=150, blank=True)
    other_info = models.CharField(max_length=150, blank=True)


class DareBigJobPilot(BaseDareBigJobPilot):
    dare_bigjob = models.ForeignKey('DareBigJob')
    time_started = models.DateTimeField()
    pilot_url = models.CharField(max_length=256, blank=True)

    def get_pilot_info(self):
        pilotdescdict = {'service_url': self.service_url,
                        'queue': self.queue,
                        'walltime': self.walltime,
                        'project': self.project,
                        'working_directory': self.working_directory,
                        'number_of_processes': self.number_of_processes,
                        'cores_per_node': self.cores_per_node
                        }
        for key in pilotdescdict.keys():
            pilotdescdict[key] = str(pilotdescdict[key])
        return pilotdescdict

    def get_stop_start(self):
        if self.status in ['New', 'Stopped', 'Canceled']:
            return True
        return False


class DareBigJobTask(BaseDareModel):
    dare_bigjob = models.ForeignKey('DareBigJob')
    dare_bigjob_pilot = models.ForeignKey('DareBigJobPilot', blank=True, null=True)
    script = models.TextField(blank=True, default=simple_task_script)
    inputfiles = models.CharField(max_length=30, blank=True)
    outputfiles = models.CharField(max_length=30, blank=True)
    cu_url = models.CharField(max_length=256, blank=True)

    def get_stop_start(self):
        if self.status in ['New', 'Stopped', 'Canceled', 'Done']:
            return True
        return False
