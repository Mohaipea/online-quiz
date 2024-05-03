from django.contrib import admin
from .models import Topics, Quiz, Question, Answer, Participants


class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'total_score', 'date']


admin.site.register(Topics)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Participants, ParticipantsAdmin)
