from django.contrib import admin
from .models import User, Transfer, Code, Solicitude, Loan

# Register your models here.

admin.site.register(User)
admin.site.register(Transfer)
admin.site.register(Code)
admin.site.register(Solicitude)
admin.site.register(Loan)
