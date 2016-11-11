from django.contrib import admin
from .models import Users, FriendStatus, FriendValue, Answers, Queries, QueriesReceived

# Register your models here.

admin.site.register(Users)
admin.site.register(FriendStatus)
admin.site.register(FriendValue)
admin.site.register(Answers)
admin.site.register(Queries)
admin.site.register(QueriesReceived)
