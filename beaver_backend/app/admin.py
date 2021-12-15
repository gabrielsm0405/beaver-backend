from django.contrib import admin
from .models import Neighborhood

class NeighborhoodAdmin(admin.ModelAdmin):
    fields = ['id', 'name']
    readonly_fields = ['id']

admin.site.register(Neighborhood, NeighborhoodAdmin)