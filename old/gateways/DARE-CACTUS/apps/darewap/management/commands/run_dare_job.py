from django.core.management.base import BaseCommand, CommandError
import os
import popen2
import time


class Command(BaseCommand):
    args = '<job_id>'
    help = "runnning a specified dare job"

    def handle(self, *args, **options):
        from django.conf import settings
        if hasattr(settings, 'dare_job_verbose'):
            self.verbose = settings.dare_job_verbose
        else:
            self.verbose = "INFO"

        job_id = args[0]

        dare_job_work_dir = 'dare_job_logs'
        if not os.path.exists(dare_job_work_dir):
            os.makedirs(dare_job_work_dir)
        self.dare_log_file = os.path.join(dare_job_work_dir, 'dare_job_%s_%s.log' % (job_id, time.strftime('%y%m%d%S')))
        self.dare_conf_file = self.do_prepare_conf_file(job_id)

        self.run_dare()

    def do_prepare_conf_file(self, outfile):
        return "path/to/conf/"

    def run_dare(self):
        args = []
        if self.verbose:
            args += ["--verbose=%s" % self.verbose]
        else:
            args += ["--verbose=INFO"]
        if self.dare_conf_file:
            args += ["%s" % self.dare_conf_file]
        if self.dare_log_file:
            args += ["--dare_log_file=%s" % self.dare_log_file]

        #pipe = popen2.Popen4('pg_dump %s > %s' % (' '.join(args), self.dare_log_file))
        #if self.passwd:
        #    pipe.tochild.write('%s\n' % self.passwd)
        #    pipe.tochild.close()
