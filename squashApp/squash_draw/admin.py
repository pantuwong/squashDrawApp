from django.contrib import admin

# Register your models here.
from .models import Player
from .models import Schedule
from .models import RankHistory

admin.site.register( Player )
admin.site.register( Schedule )
admin.site.register( RankHistory )