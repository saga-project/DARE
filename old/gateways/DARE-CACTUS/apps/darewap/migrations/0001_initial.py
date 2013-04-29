# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table('darewap_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_type', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('detail_status', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('dareprocess_id', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_jobs', null=True, to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('darewap', ['Job'])

        # Adding model 'JobInfo'
        db.create_table('darewap_jobinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(related_name='job_info', null=True, to=orm['darewap.Job'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('darewap', ['JobInfo'])

        # Adding model 'JobQueue'
        db.create_table('darewap_jobqueue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('qstatus', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('jobq_type', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(related_name='job_in_queue', null=True, to=orm['darewap.Job'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('darewap', ['JobQueue'])

        # Adding model 'UserContext'
        db.create_table('darewap_usercontext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_context', null=True, to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('usercert', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('userid', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('userkey', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('userpass', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('userproxy', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('darewap', ['UserContext'])


    def backwards(self, orm):
        # Deleting model 'Job'
        db.delete_table('darewap_job')

        # Deleting model 'JobInfo'
        db.delete_table('darewap_jobinfo')

        # Deleting model 'JobQueue'
        db.delete_table('darewap_jobqueue')

        # Deleting model 'UserContext'
        db.delete_table('darewap_usercontext')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'darewap.job': {
            'Meta': {'object_name': 'Job'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'dareprocess_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'detail_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_jobs'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'darewap.jobinfo': {
            'Meta': {'object_name': 'JobInfo'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_info'", 'null': 'True', 'to': "orm['darewap.Job']"}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'darewap.jobqueue': {
            'Meta': {'object_name': 'JobQueue'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_in_queue'", 'null': 'True', 'to': "orm['darewap.Job']"}),
            'jobq_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'qstatus': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'darewap.usercontext': {
            'Meta': {'object_name': 'UserContext'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_context'", 'null': 'True', 'to': "orm['auth.User']"}),
            'usercert': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'userkey': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'userpass': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'userproxy': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['darewap']