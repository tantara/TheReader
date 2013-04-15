from django.contrib import admin
from Broadcast.models import Game
from Broadcast.models import GameLog
from Broadcast.models import Action
from Broadcast.models import Voice
from Broadcast.models import Sound

admin.site.register(Game)
admin.site.register(GameLog)

admin.site.register(Action)
admin.site.register(Voice)
admin.site.register(Sound)
