from django.db import models
from django.utils import timezone


class Query(models.Model):
    query = models.CharField(max_length=255)
    ip = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'
        ordering = ['-timestamp']

    def __str__(self):
        if len(self.query) > 40:
            return f'{self.query[:40]}...'
        return self.query
