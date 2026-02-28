from django.contrib import admin
from .models import Dispatch, DispatchItem

admin.site.register(Dispatch)
admin.site.register(DispatchItem)