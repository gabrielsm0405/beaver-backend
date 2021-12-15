from django.db import models

class Neighborhood(models.Model):
    name = models.CharField(('name'), max_length=100, blank=False)

    class Meta:
        verbose_name = 'Neighborhood'
        verbose_name_plural = 'Neighborhoods'

    def __str__(self):
        return self.name