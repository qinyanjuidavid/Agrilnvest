from django.contrib import admin
from accounts.models import (User, Administrator)


admin.site.register(User)
admin.site.register(Administrator)
