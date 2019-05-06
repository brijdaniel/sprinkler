from crontab import CronTab
import datetime

def set(job_string, checkbox):
	cron_tab = CronTab(user='root') 

	for job in cron_tab:
		if job.comment == 'sprinkler_cron':
			job.setall(job_string)  
			cron_tab.write()

			# Enable/disable cronjob based on checkbox
			if str(checkbox) == 'True':
				job.enable()
				cron_tab.write()
			else:
				job.enable(False)
				cron_tab.write()

def next():
	now = datetime.datetime.now()
	cron_tab = CronTab(user='root') 

	for job in cron_tab:
		if job.comment == 'sprinkler_cron':    
			schedule = job.schedule(date_from=now)

	return schedule.get_next()