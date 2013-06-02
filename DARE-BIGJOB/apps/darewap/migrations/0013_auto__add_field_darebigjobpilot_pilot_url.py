# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DareBigJobPilot.pilot_url'
        db.add_column(u'darewap_darebigjobpilot', 'pilot_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DareBigJobPilot.pilot_url'
        db.delete_column(u'darewap_darebigjobpilot', 'pilot_url')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'darewap.darebigjob': {
            'Meta': {'object_name': 'DareBigJob'},
            'cordination_url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'name'", 'max_length': '30'}),
            'other_info': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'New'", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'darewap.darebigjobpilot': {
            'Meta': {'object_name': 'DareBigJobPilot'},
            'cores_per_node': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dare_bigjob': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['darewap.DareBigJob']"}),
            'data_service_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'name'", 'max_length': '30'}),
            'number_of_processes': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'pilot_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pilot_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'queue': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'service_url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'New'", 'max_length': '30'}),
            'time_started': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'walltime': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'working_directory': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        u'darewap.darebigjobtask': {
            'Meta': {'object_name': 'DareBigJobTask'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dare_bigjob': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['darewap.DareBigJob']"}),
            'dare_bigjob_pilot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['darewap.DareBigJobPilot']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inputfiles': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'name'", 'max_length': '30'}),
            'outputfiles': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'script': ('django.db.models.fields.TextField', [], {'default': '\'def tasks(NUMBER_JOBS=1):\\n    tasks = []\\n    for i in range(NUMBER_JOBS):\\n        compute_unit_description = {\\n        "executable": "/bin/echo",\\n        "arguments": ["Hello", "$ENV1", "$ENV2"],\\n        "environment": [\\\'ENV1=env_arg1\\\', \\\'ENV2=env_arg2\\\'],\\n        "number_of_processes": 4,\\n        "spmd_variation": "mpi",\\n        "output": "stdout.txt",\\n        "error": "stderr.txt"}\\n        tasks.append(compute_unit_description)\\n    return tasks\'', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'New'", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'darewap.defaultdarebigjobpilot': {
            'Meta': {'object_name': 'DefaultDareBigJobPilot'},
            'cores_per_node': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_service_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'name'", 'max_length': '30'}),
            'number_of_processes': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'pilot_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'queue': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'service_url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'New'", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'walltime': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'working_directory': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        u'darewap.job': {
            'Meta': {'object_name': 'Job'},
            'cordination_url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_jobs'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'darewap.jobdetailedinfo': {
            'Meta': {'object_name': 'JobDetailedInfo'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobinfo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_detailed_info'", 'null': 'True', 'to': u"orm['darewap.JobInfo']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'darewap.jobinfo': {
            'Meta': {'object_name': 'JobInfo'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'detail': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itype': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_info'", 'null': 'True', 'to': u"orm['darewap.Job']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'user_pilot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobuserpilots'", 'null': 'True', 'to': u"orm['darewap.UserPilots']"}),
            'user_task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobusertasks'", 'null': 'True', 'to': u"orm['darewap.UserTasks']"})
        },
        u'darewap.usercontext': {
            'Meta': {'object_name': 'UserContext'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'SSH'", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_context'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'usercert': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'userkey': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'userpass': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'userproxy': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'darewap.userpilots': {
            'Meta': {'object_name': 'UserPilots'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'detail': ('picklefield.fields.PickledObjectField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_pilots'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'darewap.userresource': {
            'Meta': {'object_name': 'UserResource'},
            'allocation': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'cores_per_node': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'data_service_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'processes_per_node': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'queue': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'service_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_resource'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'working_directory': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        u'darewap.usertasks': {
            'Meta': {'object_name': 'UserTasks'},
            'args': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'env': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'executable': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inputfiles': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'num_of_cores': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'num_of_processes': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'num_of_tasks': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'outputfiles': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'script': ('django.db.models.fields.TextField', [], {'default': '\'def tasks(NUMBER_JOBS=1):\\n    tasks = []\\n    for i in range(NUMBER_JOBS):\\n        compute_unit_description = {\\n        "executable": "/bin/echo",\\n        "arguments": ["Hello", "$ENV1", "$ENV2"],\\n        "environment": [\\\'ENV1=env_arg1\\\', \\\'ENV2=env_arg2\\\'],\\n        "number_of_processes": 4,\\n        "spmd_variation": "mpi",\\n        "output": "stdout.txt",\\n        "error": "stderr.txt"}\\n        tasks.append(compute_unit_description)\\n    return tasks\'', 'blank': 'True'}),
            'spmd_variation': ('django.db.models.fields.CharField', [], {'default': "'single'", 'max_length': '30', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_tasks'", 'null': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['darewap']