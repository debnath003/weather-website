from django.db import models

class SavedCity(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    time = models.TimeField()
    user_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('city', 'time', 'user_name')

    def __str__(self):
        return f'{self.city} - {self.user_name}'
