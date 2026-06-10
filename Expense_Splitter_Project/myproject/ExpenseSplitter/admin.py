from django.contrib import admin
from .models import User,Group,Budget,Expense

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Budget)
admin.site.register(Expense)
