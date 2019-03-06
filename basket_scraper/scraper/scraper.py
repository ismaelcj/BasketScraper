# -*- encoding: utf-8 -*-
import mechanize
# import requests
from bs4 import BeautifulSoup
from datetime import datetime


class Scraper(object):
    def __init__(self):
        self.url = 'http://gesdeportiva.fbm.es/'
        self.br = mechanize.Browser()
        self.br.addheaders = [
            ('User-agent',
             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) '
             'AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 '
             'Safari/535.7')
        ]
        self.br.open(self.url)
        self.br.select_form(nr=0)
        self.competition_id, self.competition_name = self.get_current_competition()
        self.category_id, self.category_name = self.get_current_category()
        self.phase_id, self.phase_name = self.get_current_phase()
        self.group_id, self.group_name = self.get_current_group()

    def submit(self):
        self.br.submit()
        self.br.select_form(nr=0)

    def get_competitions(self):
        competitions_raw = self.br.form.find_control('DDLCompeticiones').get_items()
        competitions = [{
            'id': item.attrs.get('value'),
            'name': item.attrs.get('label')
        } for item in competitions_raw]
        return competitions

    def get_current_competition(self):
        competitions = self.br.form.find_control('DDLCompeticiones').get_items()
        for item in competitions:
            if item.attrs.get('selected', False):
                return item.attrs.get('value'), item.attrs.get('label')

    def set_competition(self, competition_num):
        if self.competition_id == competition_num:
            return
        self.competition_id = competition_num
        self.br.form.set_value([competition_num], 'DDLCompeticiones')
        self.submit()

    def get_categories(self):
        categories_raw = self.br.form.find_control('DDLCategorias').get_items()
        categories = [{
            'id': item.attrs.get('value'),
            'name': item.attrs.get('label')
        } for item in categories_raw]
        return categories

    def get_current_category(self):
        categories = self.br.form.find_control('DDLCategorias').get_items()
        for item in categories:
            if item.attrs.get('selected', False):
                return item.attrs.get('value'), item.attrs.get('label')

    def set_category(self, category_num):
        if self.category_id == category_num:
            return
        self.category_id = category_num
        self.br.form.set_value([category_num], 'DDLCategorias')
        self.submit()

    def get_phases(self):
        phases_raw = self.br.form.find_control('DDLFases').get_items()
        phases = [{
            'id': item.attrs.get('value'),
            'name': item.attrs.get('label')
        } for item in phases_raw]
        return phases

    def get_current_phase(self):
        phases = self.br.form.find_control('DDLFases').get_items()
        for item in phases:
            if item.attrs.get('selected', False):
                return item.attrs.get('value'), item.attrs.get('label')

    def set_phase(self, phase_num):
        if self.phase_id == phase_num:
            return
        self.phase_id = phase_num
        self.br.form.set_value([phase_num], 'DDLFases')
        self.submit()

    def get_groups(self):
        groups_raw = self.br.form.find_control('DDLGrupos').get_items()
        groups = [{
            'id': item.attrs.get('value'),
            'name': item.attrs.get('label')
        } for item in groups_raw]
        return groups

    def get_current_group(self):
        groups = self.br.form.find_control('DDLGrupos').get_items()
        for item in groups:
            if item.attrs.get('selected', False):
                return item.attrs.get('value'), item.attrs.get('label')

    def set_group(self, group_num):
        if self.group_id == group_num:
            self.submit()
        self.group_id = group_num
        self.br.form.set_value([group_num], 'DDLGrupos')
        self.submit()

    def get_teams(self):
        bs = BeautifulSoup(self.br.response().read(), "html.parser")
        teams_raw = bs.find(id='equipos')
        team_rows = teams_raw.findAll('tr')
        teams = {}
        for row in team_rows[1:]:
            team_info = row.findAll('td')
            team_name = team_info[0].text
            teams[team_name] = {
                'name': team_name,
                'competition_id': self.competition_id,
                'competition_name': self.competition_name,
                'category_id': self.category_id,
                'category_name': self.category_name,
                'phase_id': self.phase_id,
                'phase_name': self.phase_name,
                'group_id': self.group_id,
                'group_name': self.group_name,
                'city': team_info[1].text,
                'color': team_info[2].text,
                'color2': team_info[3].text,
            }
        classification_raw = bs.find(id='PClasificacion')
        classification_rows = classification_raw.findAll('tr')
        for row in classification_rows[1:]:
            team_info = row.findAll('td')
            name = team_info[1].text
            # import pdb; pdb.set_trace()
            if name in teams:
                teams[name].update({
                    'position': team_info[0].text,
                    'matches_played': team_info[2].text,
                    'matches_won': team_info[3].text,
                    'matches_lost': team_info[4].text,
                    'points_for': team_info[5].text,
                    'points_against': team_info[6].text,
                    'points_total': team_info[7].text,
                })
        return teams


def get_teams(competition_id, category_id, phase_id, group_id):
    sp = Scraper()
    sp.set_competition(competition_id)
    sp.set_category(category_id)
    sp.set_phase(phase_id)
    sp.set_group(group_id)
    teams = sp.get_teams()
    return teams
