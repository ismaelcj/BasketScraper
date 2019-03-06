import mechanize
from bs4 import BeautifulSoup
url = 'http://gesdeportiva.fbm.es/'
br = mechanize.Browser()
br.addheaders = [
    ('User-agent',
     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) '
     'AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 '
     'Safari/535.7')
]
br.open(url)
br.select_form(nr=0)

for item in br.form.find_control('DDLCompeticiones').get_items():
    print("\t{} | {} | {}".format(item.name, item.attrs['label'], item.attrs.get('selected', '')))

for item in br.form.find_control('DDLCategorias').get_items():
    print("\t{} | {} | {}".format(item.name, item.attrs['label'], item.attrs.get('selected', '')))

for item in br.form.find_control('DDLFases').get_items():
    print("\t{} | {} | {}".format(item.name, item.attrs['label'], item.attrs.get('selected', '')))

for item in br.form.find_control('DDLGrupos').get_items():
    print("\t{} | {} | {}".format(item.name, item.attrs['label'], item.attrs.get('selected', '')))

name = "CB GETAFE ´A´"
com = '15471'
cat = '15610'
fas = '69'
gru = '228'

br.form.set_value([com], 'DDLCompeticiones')
br.submit()
br.select_form(nr=0)
br.form.set_value([cat], 'DDLCategorias')
br.submit()
br.select_form(nr=0)
br.form.set_value([fas], 'DDLFases')
br.form.set_value([gru], 'DDLGrupos')

bs = BeautifulSoup(br.response().read(), "html.parser")

teams = bs.find(id='equipos')
team_rows = teams.findAll('tr')
for row in team_rows[1:]:
    columns = row.findAll('td')
    team = columns[0].text
    city = columns[1].text
    color = columns[2].text
    color2 = columns[3].text
    print("\t{} | {} | {} | {}".format(team, city, color, color2))

ppartidos = bs.find(id='PProximosPartidos')
ppartidos_rows = ppartidos.findAll('tr')
for row in ppartidos_rows[1:]:
    columns = row.findAll('td')
    unk = columns[0].text
    loc = columns[1].text
    vis = columns[2].text
    fec = columns[3].text
    cam = columns[4].text
    print("\t{} | {} | {} | {} | {}".format(unk, loc, vis, fec, cam.replace('\n', '')))

ultima = bs.find(id='PUltimaJornada')
ultima_rows = ultima.findAll('tr')
for row in ultima_rows[1:]:
    columns = row.findAll('td')
    fec = columns[1].text
    loc_res = columns[2].text
    loc = columns[3].text
    vis = columns[4].text
    vis_res = columns[5].text
    print("\t{} | {} | {}-{} | {}".format(fec, loc, loc_res, vis_res, vis))
