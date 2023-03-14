import datetime
from typing import OrderedDict
from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    url = models.URLField(null=True, blank=True)
    date_applied = models.DateField(("Date"), default=datetime.date.today)
    STAGES = [('JOBAPPLIED', 'Job Applied'), ('HRCALL', 'HR call'),
              ('FSTINT', 'First Interview'),
              ('SNDINT', 'Second Interview'),
              ('TRDINT', 'Third Interview'),
              ('JOBOFFER', 'Job Offer'),
              ('DENIED', 'Denied')
              ]
    stage = models.CharField(max_length=10,
                             choices=STAGES, default='JOBAPPLIED')
    notes = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title

    class Meta:
        ordering = ['-date_applied']
