# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from basket_scraper.scraper.scraper import Scraper
from basket_scraper.models import Category, Competition, Group, Phase, Team, TeamPhase

from pprint import pprint


class Command(BaseCommand):
    help = 'Populates the teams with the scrapped datas'

    def handle(self, *args, **options):
        sp = Scraper()
        for comp in sp.get_competitions():
            competition = Competition.get_or_create(comp.get('id'), comp.get('name'))
            sp.set_competition(competition.feb_id)
            for cat in sp.get_categories():
                category = Category.get_or_create(cat.get('id'), cat.get('name'))
                sp.set_category(category.feb_id)
                for pha in sp.get_phases():
                    phase = Phase.get_or_create(pha.get('id'), pha.get('name'))
                    sp.set_phase(phase.feb_id)
                    for gro in sp.get_groups():
                        group = Group.get_or_create(gro.get('id'), gro.get('name'))
                        sp.set_group(group.feb_id)
                        teams = sp.get_teams()
                        for team_key in teams:
                            Team.create_or_update_team(
                                teams[team_key], competition, category, group,
                                phase)
