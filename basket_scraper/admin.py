from django.contrib import admin
from basket_scraper.models import Team, TeamPhase

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'competition', 'category', 'city')
    list_filter = ('competition', 'category', 'city')
    search_fields = ('name',)

class TeamPhaseAdmin(admin.ModelAdmin):
    search_fields = ('phase__name', 'team__name')


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamPhase, TeamPhaseAdmin)
