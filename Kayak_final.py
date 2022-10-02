
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = 'iframe_connected'
import plotly.express as px
import requests
import re
from math import *
import pandas as pd
import json

pip install scrapy

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',

import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.shell import inspect_response

class Booking(scrapy.Spider):
    name = "Booking"
    cities = ["Mont-Saint-Michel","St-Malo", "Bayeux","Le-Havre","Rouen","Paris","Amiens","Lille","Strasbourg",
"Chateau-du-Haut-Koenigsbourg","Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon",
"Gorges-du-Verdon","Bormes-les-Mimosas","Cassis","Marseille","Aix-en-Provence","Avignon","Uzes","Nimes",
"Aigues-Mortes","Saintes-Maries-de-la-mer","Collioure","Carcassonne","Ariege","Toulouse","Montauban","Biarritz",
"Bayonne","La-Rochelle"]
    
    def start_requests(self):
        start_urls = [f'https://www.booking.com/searchresults.fr.html?ss={i}&rows=25&offset=0&order=score' for i in self.cities]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers, 
                                 meta = {'url1' : url})

    def parse(self, response):
        url1 = response.meta['url1']
        for href in response.css("h3 > a::attr('href')"):
            link = response.urljoin(href.extract())
            if "searchresults#hotelTmpl" in link and "https://www.booking.com/hotel/fr" in link and any(i in link for i in ['hpos=' + str(i) + '&' for i in range(1,21)]):             
                yield scrapy.Request(url = link, callback = self.parse2, headers=headers, 
                                 meta={'url1' : url1})

    def parse2(self, response):
        url1 = response.meta['url1']
        hotels = response.xpath("//h2[@class='hp__hotel-name']")
        adresses = response.xpath("//p[@class='address address_clean']/span")
        ratings = response.xpath("//div[@class='b5cd09854e d10a6220b4']")
        raters = response.xpath("//div[@class='d8eab2cf7f c90c0a70d3 db63693c62']")
        latlon = response.xpath("//a[@id='hotel_address']")
        desc = response.xpath("//div[@id='property_description_content']")
        for i in range(len(hotels)):
            yield{
                'adresse': adresses[i].css('::text').extract()[0].strip(),
                'url1' : url1,
                'url': response.url,
                'name': hotels[i].css('::text').extract()[2].strip(),
                'rater': raters[i].css('::text').extract()[0].strip(),  
                'rating': ratings[i].css('::text').extract(), 
                'latlong': latlon[i].css('::attr("data-atlas-latlng")').extract(),
                'description': desc[i].css('::text').extract()    
            }
                
filename = "data_hotels.json"

if filename in os.listdir('/'):
        os.remove('/' + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'custom user agent',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'src/' + filename : {"format": "json"},
    }
})

process.crawl(Booking)
process.start()

df = pd.read_json('data_hotels.json', lines=False)
df['ville'] = ''
df['lat'] = ''
df['long'] = ''
for i in range(len(df)):
    df.ville[i] = re.search("ss=(.+?)&rows",df.url1[i]).group(1).capitalize()
    df.rating[i] = float(df.rating[i][0].replace(",", "."))
    df.rater[i] = df.rater[i]
    df.lat[i] = float(df.latlong[0][0].split(',')[0])
    df.long[i] = float(df.latlong[0][0].split(',')[1])
df.drop(['url','url1'], axis = 1, inplace=True)
df.to_json('data_hotels_cleaned.json', orient='columns')


df_final = pd.read_json('data_hotels_cleaned.json', lines=True)

# ## Utilisation API MétéoConcept et Mapbox
# Pour l'utilisation des cartes avec <b>Plotly</b>, j'ai utilisé le service de Mapbox qui permet d'obtenir des cartes personnalisées <br/>
# Pour la météo, j'ai choisi l'API de <b>MétéoConcept</b> (gratuite) qui permet de récupérer des données en temps réel et aussi sur 14 jours 
token = 'pk.eyJ1IjoieWFubm91c2giLCJhIjoiY2t6ZTc5ZjRnMGY0djJ1b2NmbXR2OXlhcSJ9.TyZxcshIKgaeIkY9p5LkdQ'

fig = px.scatter_mapbox(df_final, lat="lat", 
                        lon="lon",
                        hover_name=df_final['name'], 
                        zoom=4, 
                        color=df_final['rating'])
fig.update_layout(
    mapbox_style="mapbox://styles/yannoush/ckze79qfr007714qekbj3styn", showlegend=False, mapbox_accesstoken=token, title='Hôtels des 35 villes les plus visitées de France',title_x=0.5)
fig.show()

villes_insee = [50353,35288,14047,76351,76540,75101,80021,59350,67482,67362,68066,68078,25056,21231,74010,38185,
69381,83019,13022,13201,13001,84007,30334,30189,30003,13096,66053,11069,31555,82121,64122,64102,17300]

meteo_liste = []
for x in villes_insee:
    response = requests.get('https://api.meteo-concept.com/api/forecast/daily/0?token=f454f3c826fbd1cdbc876142c58201f98e13861e4d2ef76f299f6fa8e867b43f&insee={}'.format(x))
    meteo = json.loads(response.content)
    meteo_liste.append(meteo)
response = requests.get('https://api.meteo-concept.com/api/forecast/daily/0?token=f454f3c826fbd1cdbc876142c58201f98e13861e4d2ef76f299f6fa8e867b43f&insee=04186')
meteo = json.loads(response.content)
meteo_liste.append(meteo)
response = requests.get('https://api.meteo-concept.com/api/forecast/daily/0?token=f454f3c826fbd1cdbc876142c58201f98e13861e4d2ef76f299f6fa8e867b43f&insee=09122')
meteo = json.loads(response.content)
meteo_liste.append(meteo)

meteo_bis = []
villes_meteo = []
for i in range(0, len(meteo_liste)):
    meteo_bis.append(meteo_liste[i]['forecast'])
    villes_meteo.append(meteo_liste[i]['city']['name'])
pluie = {}

icon_list = []
transi = ''
j = 0
for i in df_meteo['probarain']:
    if i > 70:
        icon_list.append("🌧")
    if i >= 30:
        icon_list.append('⛅')
    else:
        icon_list.append('🌞')
    if df_meteo['wind10m'][j] > 50:
        transi = icon_list[j]
        icon_list[j] = transi + " 💨"
    j+= 1
fig_meteo = go.Figure(go.Scattermapbox(lat=df_meteo["latitude"], 
                        lon=df_meteo["longitude"],
                        mode='markers',
                        marker=go.scattermapbox.Marker(size=12, color =  df_meteo['tmax'], colorscale = 'Blackbody_r'),
                        hoverinfo="text",
                        textposition='top right',
                        textfont=dict(size=20, color='black'),
                        text=[icon_list[i]+ '<br>' + df_meteo['ville'][i] + '<br>' + str(df_meteo['tmax'][i])+"°C" + '<br>' for i in range(df_meteo.shape[0])]))
fig_meteo.update_layout(mapbox_style="mapbox://styles/yannoush/ckze79qfr007714qekbj3styn", showlegend=False, mapbox_accesstoken=token, hoverlabel=dict(font_size=20), title='Météo des 35 villes les plus visitées de France', title_x=0.5)
fig_meteo.show()


# ## Récupération de la meilleure ville pour voyager

# #### Récupération des données à la semaine

meteobis_liste = []

for x in villes_insee:
    response = requests.get('https://api.meteo-concept.com/api/forecast/daily?token=f454f3c826fbd1cdbc876142c58201f98e13861e4d2ef76f299f6fa8e867b43f&insee={}&start=0&end=7'.format(x))
    meteobis = json.loads(response.content)
    meteobis_liste.append(meteobis)
response = requests.get('https://api.meteo-concept.com/api/forecast/daily?token=f454f3c826fbd1cdbc876142c58201f98e13861e4d2ef76f299f6fa8e867b43f&insee=04186&start=0&end=7')
meteobis = json.loads(response.content)
meteobis_liste.append(meteobis)
response = requests.get('https://api.meteo-concept.com/api/forecast/daily?token=f454f3c826fbd1cdbc876142c58201f98e13861e4d2ef76f299f6fa8e867b43f&insee=09122&start=0&end=7')
meteobis = json.loads(response.content)
meteobis_liste.append(meteobis)


# #### Création dataset pour notation du score météo
# On fait une moyenne pondérée pour deux variables (temps d'ensoleillement et quantité de pluie dans les 7 prochains jours)

df_meteobis = pd.DataFrame(meteobis_liste)
score_meteo_sun = []
score_meteo_rain = []
for i in range(0,35):
    temp_score_sun = 0
    temp_score_rain = 0
    for j in range(0,8):
        temp_score_sun += df_meteobis['forecast'][i][j]['sun_hours']
        temp_score_rain += df_meteobis['forecast'][i][j]['rr10']
    score_meteo_sun.append(temp_score_sun)
    score_meteo_rain.append(temp_score_rain)


# #### Métrique pour la notation + ranking par ville

max_sun = max(score_meteo_sun)
for i in range(0, len(score_meteo_sun)):
    score_meteo_sun[i] = score_meteo_sun[i]/max_sun*100
max_rain= max(score_meteo_rain)
for i in range(0, len(score_meteo_rain)):
    score_meteo_rain[i] = 100-(score_meteo_rain[i]/max_rain*100)
score_df = pd.DataFrame(score_meteo_sun, columns=['sun'])
score_df['rain'] = score_meteo_rain
score_df['note'] = [(i+j) / 20 for i,j in zip(score_meteo_sun, score_meteo_rain)]
score_df['rank'] = score_df['note'].rank(method='dense', ascending=False)

meteo_bis = []
villes_meteo = []
for i in range(0, len(meteo_liste)):
    meteo_bis.append(meteo_liste[i]['forecast'])
    villes_meteo.append(meteo_liste[i]['city']['name'])
pluie = {}
df_meteo = pd.DataFrame(meteo_bis)
df_meteo['weather_score'] = score_df['note']
df_meteo['ville'] = villes_meteo
df_meteo['rank'] = score_df['rank']
df_meteo.head()


# #### Affichage des hôtels de la top destination

lat_nice_wther = df_meteo['latitude'][df_meteo['rank'] == 1].iloc[0]
long_nice_wther = df_meteo['longitude'][df_meteo['rank'] == 1].iloc[0]
city_nice_wther = df_meteo['ville'][df_meteo['rank'] == 1].iloc[0]

from datetime import date
today = date.today()

fig = px.scatter_mapbox(df_final, lat="lat", 
                        lon="lon",
                        hover_name=df_final['name'], 
                        zoom=12, 
                        color=df_final['rating'],
                        center = {'lat':lat_nice_wther,'lon':long_nice_wther},
                        title = 'Hôtels de la top destination : {} - T° = {}°C'.format(city_nice_wther, df_meteo['tmax'][df_meteo['rank'] == 1].iloc[0]))
fig.update_layout(mapbox_style="mapbox://styles/yannoush/ckze79qfr007714qekbj3styn", showlegend=False, mapbox_accesstoken=token, title_x=0.5, margin=dict(l=20, r=20, t=30, b=5))
fig.show()
print('Autres villes dans le TOP 5 des destinations pour la semaine du {} : {}'.format(today.strftime("%d/%m/%Y"),', '.join(df_meteo['ville'][(df_meteo['rank'] <= 5) & (df_meteo['rank'] > 1)].tolist()[:5])))


# ## ETL - Boto3, SQLAlchemy


import boto3
session = boto3.Session(aws_access_key_id="JEAN_ACCESS_KEY", 
                        aws_secret_access_key="JEAN_SECRET_ACCESS_KEY")

s3 = session.resource("s3")
bucket_name =s3.create_bucket(Bucket="jedha-jean-kayak-project")

csv = df_final.to_csv()

put_object = bucket_name.put_object(Key="data_hotels_cleaned.csv", Body = csv)

    
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://YOUR_USERNAME:YOUR_PASSWORD@YOUR_HOSTNAME/postgres", echo=True)

from sqlalchemy.sql import text

conn = engine.connect()

df_final.to_sql("villes", engine)




