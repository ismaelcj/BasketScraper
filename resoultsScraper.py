# -*- encoding: utf-8 -*-
import mechanize
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class ResoultsScraper(object):
    def __init__(self, federation_num):
        self.url = "http://competiciones.feb.es/autonomicas/" \
                   "Resultados.aspx?a={}".format(federation_num)
        self.default_season = '2016'
        self.br = mechanize.Browser()
        self.br.addheaders = [
            ('User-agent',
             'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) '
             'AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 '
             'Safari/535.7')
        ]
        self.br.open(self.url)
        self.br.select_form(nr=0)

        self.ctrl = {
            'season': 'controlNavegacion:temporadasDropDownList',
            'category': 'controlNavegacion:categoriasDropDownList',
            'group': 'gruposDropDownList',
            'round': 'jornadasDropDownList'
        }
        self.set_season(self.default_season)

    def get_seasons(self):
        items_raw = self.br.form.find_control(self.ctrl['season']).get_items()
        return {int(i.name): i.attrs.get('label', '') for i in items_raw}

    def set_season(self, season):
        self.br.form[self.ctrl['season']] = [str(season)]
        self.br.submit()
        self.br.select_form(nr=0)

    def get_categories(self):
        items_raw = self.br.form.find_control(self.ctrl['category']).get_items()
        return {int(i.name): i.attrs.get('label', '') for i in items_raw}

    def set_category(self, category):
        self.br.form[self.ctrl['category']] = [unicode(category)]
        self.br.submit()
        self.br.select_form(nr=0)

    def get_groups(self):
        items_raw = self.br.form.find_control(self.ctrl['group']).get_items()
        return {int(i.name): i.attrs.get('label', '') for i in items_raw}

    def set_group(self, group):
        self.br.form[self.ctrl['group']] = [unicode(group)]
        self.br.submit()
        self.br.select_form(nr=0)

    def get_teams(self):
        bs = BeautifulSoup(self.br.response().read(), "html.parser")
        teams_raw = bs.findAll('a', {'class': 'linkEquipo'})
        teams = {}
        for team in teams_raw:
            params_raw = team['href'].replace('Rachas.aspx?', '').split('&')
            params = {pair[0]: pair[1] for pair in [
                param.split('=') for param in params_raw]}
            teams.update({
                int(params['i']): {
                    'name': team.text.strip().replace(u'Â', ''),
                    'url': team['href']
                }
            })
        return teams

    def get_teams_by_name(self):
        bs = BeautifulSoup(self.br.response().read(), "html.parser")
        teams_raw = bs.findAll('a', {'class': 'linkEquipo'})
        teams = {}
        for team in teams_raw:
            params_raw = team['href'].replace('Rachas.aspx?', '').split('&')
            params = {pair[0]: pair[1] for pair in [
                param.split('=') for param in params_raw]}
            teams.update({
                team.text.strip().replace(u'Â', ''): {
                    'id': int(params['i']),
                    'url': team['href']
                }
            })
        return teams

    def get_resoults(self):
        bs = BeautifulSoup(self.br.response().read(), "html.parser")
        table_raw = bs.find(id='jornadaDataGrid')
        rows = table_raw.findAll('tr')
        table = []
        resoults = []
        for row in rows:
            columns = row.findAll('td')
            table.append(tuple(
                column.text.strip().replace(u'Â', '') for column in columns))
        for row in table:
            tm1, tm2 = row[0].split(' - ')
            pts_tm1, pts_tm2 = row[1].split('-')
            teams = self.get_teams_by_name()
            tm1_id = teams[tm1]['id']
            tm2_id = teams[tm2]['id']
            resoults.append([(tm1_id, tm1, pts_tm1), (tm2_id, tm2, pts_tm2)])
        return resoults

    def get_classification(self):
        bs = BeautifulSoup(self.br.response().read(), "html.parser")
        table_raw = bs.find(id='clasificacionDataGrid')
        rows = table_raw.findAll('tr')
        table = []
        for row in rows:
            columns = row.findAll('td')
            table.append(tuple(
                column.text.strip().replace(u'Â', '') for column in columns))
        return table

    def get_rounds(self):
        items_raw = self.br.form.find_control(self.ctrl['round']).get_items()
        rounds = {int(i.name): i.attrs.get('label', '') for i in items_raw}
        for rnd, value in rounds.iteritems():
            values = value.split(' ')
            rounds[rnd] = {
                'name': ' '.join(values[:-1]),
                'complete_name': value,
                'date': datetime.strptime(values[-1], "%d/%m/%Y")
            }
        return rounds

    def set_round(self, round):
        self.br.form[self.ctrl['round']] = [unicode(round)]
        self.br.submit()
        self.br.select_form(nr=0)

    def get_next_round(self):
        this_week_match = self.this_week_match()
        next_week_match = self.next_week_match()
        return this_week_match + next_week_match

    def this_week_match(self):
        bs = BeautifulSoup(self.br.response().read(), "html.parser")
        table_raw = bs.find(id='jornadaDataGrid')
        if not table_raw:
            # print "**** NO NEXT ROUND ****"
            return []
        rows = table_raw.findAll('tr')
        table = []
        next_round = []
        for row in rows:
            columns = row.findAll('td')
            table.append(tuple(
                column.text.strip().replace(u'Â', '') for column in columns))
        for row in table:
            bs_teams = BeautifulSoup(row[0], "html.parser")
            teams = bs_teams.contents[0]
            tm1, tm2 = teams.split(' - ')
            pts_tm1, pts_tm2 = row[1].split('-')
            # import pdb; pdb.set_trace()
            teams = self.get_teams_by_name()
            tm1_id = teams[tm1]['id']
            tm2_id = teams[tm2]['id']
            next_round.append({
                'home_team_id': tm1_id,
                'home_team': tm1,
                'pts_home_team': pts_tm1 or False,
                'visitor_id': tm2_id,
                'visitor': tm2,
                'pts_visitor': pts_tm2 or False,
                'date': datetime.strptime(
                    "{} {}".format(row[2], row[3]),
                    '%d/%m/%Y %H:%M'),
                'field_id': False,
                'field': False
            })
        return next_round

    def next_week_match(self):
        bs = BeautifulSoup(self.br.response().read(), "html.parser")
        table_raw = bs.find(id='proximaJornadaDataGrid')
        if not table_raw:
            # print "**** NO NEXT ROUND ****"
            return []
        rows = table_raw.findAll('tr')
        table = []
        next_round = []
        for row in rows:
            columns = row.findAll('td')
            table.append(tuple(
                column.text.strip().replace(u'Â', '') for column in columns))
        for row in table:
            bs_teams = BeautifulSoup(row[0], "html.parser")
            teams, field = bs_teams.contents[0].split('\nCampo: ')
            fields_split = field.split('-')
            field_id = fields_split[0]
            field = '-'.join(fields_split[1:])
            tm1, tm2 = teams.split(' - ')
            pts_tm1, pts_tm2 = row[1].split('-')
            # import pdb; pdb.set_trace()
            teams = self.get_teams_by_name()
            tm1_id = teams[tm1]['id']
            tm2_id = teams[tm2]['id']
            next_round.append({
                'home_team_id': tm1_id,
                'home_team': tm1,
                'pts_home_team': pts_tm1 or False,
                'visitor_id': tm2_id,
                'visitor': tm2,
                'pts_visitor': pts_tm2 or False,
                'date': datetime.strptime(
                    "{} {}".format(row[2], row[3]),
                    '%d/%m/%Y %H:%M'),
                'field_id': field_id,
                'field': field
            })
        return next_round


if __name__ == '__main__':
    scraper = ResoultsScraper()
    scraper.set_category(13250)
    rounds = scraper.get_rounds()
