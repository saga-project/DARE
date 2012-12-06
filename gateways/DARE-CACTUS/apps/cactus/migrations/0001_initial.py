# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Thornfiles'
        db.create_table('cactus_thornfiles', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('thornfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_thorns', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('cactus', ['Thornfiles'])

        # Adding model 'Paramfiles'
        db.create_table('cactus_paramfiles', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('paramfile', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(related_name='job_params', to=orm['darewap.Job'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('cactus', ['Paramfiles'])


    def backwards(self, orm):
        # Deleting model 'Thornfiles'
        db.delete_table('cactus_thornfiles')

        # Deleting model 'Paramfiles'
        db.delete_table('cactus_paramfiles')


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
        'cactus.paramfiles': {
            'Meta': {'object_name': 'Paramfiles'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_params'", 'to': "orm['darewap.Job']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'paramfile': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'cactus.thornfiles': {
            'Meta': {'object_name': 'Thornfiles'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'thornfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_thorns'", 'to': "orm['auth.User']"})
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
        }
    }

    complete_apps = ['cactus']