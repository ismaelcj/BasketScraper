from django.db import models


class FebModel(models.Model):
    feb_id = models.CharField(max_length=10)
    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return "{}".format(self.name)

    @classmethod
    def get_or_create(cls, feb_id, name):
        obj = cls.objects.filter(feb_id=feb_id)
        if not obj:
            obj = cls(
                feb_id=feb_id,
                name=name,
            )
            obj.save()
        elif len(obj) > 1:
            raise Exception("More than one {} found for name: '{}'".format(
                cls.__name__, name))
        else:
            obj = obj.first()
        return obj


class Competition(FebModel):
    pass


class Category(FebModel):
    pass


class Phase(FebModel):
    pass


class Group(FebModel):
    pass


class Team(FebModel):
    feb_id = models.CharField(max_length=10, null=True, blank=True)
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=80, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    color2 = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'category')

    @classmethod
    def create_or_update_team(cls, team_data, competition, category, group, phase):
        name = team_data.get('name')
        team = Team.objects.filter(name=name)
        if team:
            if len(team) == 1:
                team = team[0]
        else:
            team = Team(
                name=name,
                competition=competition,
                category=category,
                city=team_data.get('city'),
                color=team_data.get('color'),
                color2=team_data.get('color2'),
            )
            team.save()
            print("[NEW TEAM] {} | com: {} | cat: {}".format(
                team.name, team.competition_id, team.category_id))
        team_phase = TeamPhase.objects.filter(phase_id=phase.id, team_id=team.id)
        if not team_phase:
            team_phase = TeamPhase(
                team=team,
                phase=phase,
                group=group,
                matches_played=team_data.get('matches_played'),
                matches_won=team_data.get('matches_won'),
                matches_lost=team_data.get('matches_lost'),
                position=team_data.get('position'),
                points_for=team_data.get('points_for'),
                points_against=team_data.get('points_against'),
                points_total=team_data.get('points_total'),
            )
            team_phase.save()
            print("[NEW TEAM PHASE] id: {} | team: {}".format(
                team_phase.id, team_phase.team.name))


class TeamPhase(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='phases')
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    matches_played = models.IntegerField()
    matches_won = models.IntegerField()
    matches_lost = models.IntegerField()
    position = models.IntegerField()
    points_for = models.IntegerField()
    points_against = models.IntegerField()
    points_total = models.IntegerField()

    class Meta:
        unique_together = ('team', 'group')

    def __str__(self):
        return "{} - {} - {}".format(
            self.team.name, self.team.category.name, self.phase.name)
