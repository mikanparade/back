from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='calendars', on_delete=models.CASCADE)

    def to_updated(self, data: dict) -> 'Calendar':
        if 'name' in data:
            self.name = data['name']
        if 'color' in data:
            self.color = data['color']
        return self

class Event(models.Model):
    summary = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    rrule = models.CharField(max_length=255, null=True, blank=True)
    exclude_date = models.JSONField(default=list)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    recurrence_id = models.DateTimeField()

    calendar = models.ForeignKey(Calendar, related_name='events', on_delete=models.CASCADE)

    def to_updated(self, data: dict) -> 'Event':
        if 'summary' in data:
            self.name = data['summary']
        if 'description' in data:
            self.color = data['description']
        if 'start' in data:
            self.start = data['start']
        if 'end' in data:
            self.end = data['end']
        if 'rrule' in data:
            self.rrule = data['rrule']
        if 'exclude_data' in data:
            self.exclude_date = data['exclude_data']
        if 'recurrence_id' in data:
            self.recurrence_id = data['recurrence_id']
        return self
