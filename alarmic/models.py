from django.db import models
from django.conf import settings

class Alarm(models.Model):
    time = models.TimeField()
    description = models.CharField(max_length=250, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sound = models.CharField(max_length=100, default='default_alarm.mp3')

    def __str__(self):
        return f"Alarm at {self.time} - {self.description}"
    
    @property
    def sound_path(self):
        return f"{settings.MEDIA_ROOT}/alarm_sounds/{self.sound}"