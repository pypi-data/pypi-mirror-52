import os
import logging
from datetime import datetime
from threading import Thread
from django.conf import settings

from process.models import Job, JobTask
logger = logging.getLogger('django-process')

tasks_logs_dir = getattr(settings, 'DJ_PROCESS_LOGS_DIR', None)


class TaskThreaded(Thread):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = obj

    def run(self):
        try:
            # mark task instance as initialized
            self.obj.dt_start = datetime.now()
            self.obj.status = JobTask.initialized
            self.obj.save()

            try:
                response = {}
                task_logger = None
                if tasks_logs_dir and self.obj.task.log_file:
                    file = self.obj.task.log_file \
                        if self.obj.task.log_file.endswith('.log') else f'{self.obj.task.log_file}.log'
                    log_file = os.path.join(tasks_logs_dir, file)
                    logging.basicConfig(filename=log_file, filemode='a',
                                        format='%(asctime)s %(message)s',
                                        level=logging.DEBUG)
                    task_logger = logging.getLogger()
                    response['logger'] = task_logger

                exec(self.obj.task.code, globals(), response)

                if task_logger is not None:
                    task_logger.handlers[0].flush()

                # if no observations returned always save a string in attribute
                self.obj.observations = response.get('observations', '')
                if response.get('error'):
                    raise Exception(' task response with error ')

                self.obj.status = JobTask.finished

            except Exception as e:
                # if error send to logger and also mark task and it's job as error
                self.obj.observations += f' exception when running task {e}'
                self.obj.status = JobTask.error
                self.obj.job.status = Job.error
                logger.error(f'task {self.obj} finished with error {self.obj.observations}')
                self.obj.job.save()

            self.obj.dt_end = datetime.now()
            self.obj.save()
        except Exception as e:
            logger.exception(f'error {e} when processing task {self.obj}')
