from django.contrib import admin
from django.db import connection

from .models import (Pepole, QA,  )

from django.contrib import admin

# Register your models here.
class pepoleAdmin(admin.ModelAdmin):

    list_display = ('owner', 'user_type', 'first_name', 'last_name', 'user_id')
    fieldsets = (
        (None, {'fields': (
            'owner', 'user_type', 'first_name', 'last_name', 'user_id',
            ), }
         ),)

    list_filter = ['user_type']
    search_fields = ['last_name']




class QaAdmin(admin.ModelAdmin):
    list_display = ('owner','qa_type','title', 'content', 'category')

    fieldsets = (
        (None, {'fields': ('owner','qa_type','title', 'content', 'category'), }
         ),
        ('اطلاعات اضافی', {
            'classes': ('collapse',),
            'fields': ('ref','pepole'),
        }),
    )

    list_filter = ['qa_type', 'title']


admin.site.register(QA, QaAdmin)
admin.site.register(Pepole, pepoleAdmin)
