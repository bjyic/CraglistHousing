import datetime
import pandas as pd
import datetime
import os
import geopy.distance
from geopy.distance import great_circle
now = datetime.datetime.now()
output_date=str(now.year)+str(now.month)+str(now.day-1)

import pandas as pd
pd.set_option('display.max_colwidth', -1)



def delete_map(x):
    try:
        return str(x).replace('()','').strip()
    except:
        return ''

from flask import Flask, render_template, request, redirect 
app = Flask(__name__)

pd.set_option('display.max_colwidth', -1)
@app.route('/')
def main():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    else:
        address_input = request.form['address_input']
        radius_input= request.form['radius_input']
        if len(address_input.strip())>4 :
            def target_location_check (x):
                global target_location_coords
                from geopy.geocoders import Nominatim
                geolocator = Nominatim()
                target_location=geolocator.geocode(x)
                target_location_coords=(target_location.latitude,target_location.longitude)
                print_address=target_location.address
                return target_location_coords,print_address
            
            target_location_coords,print_address=target_location_check(address_input)
            #print print_address
            #print target_location_coords
            

            data_pre=pd.read_csv(r"C:\Users\cnyi\Box Sync\Github\Python-code\CraglistHousing\apa_data_final.csv",encoding ='utf8',index_col=None)
            data_pre['mapaddress']=data_pre['mapaddress'].str.replace('\n','').str.replace(r'(google map)','').str.strip().str.replace('()','')
            data_pre['mapaddress']=data_pre['mapaddress'].apply(lambda x : delete_map(x))
            data_pre['url']=data_pre['url'].apply(lambda x: r'<a href="'+x+'">link</a>')
            
            def great_circle_distance(x):
                global target_location_coords
                import sys
                try:
                    distance=great_circle(target_location_coords,x).miles
                   # print target_location_coords
                except:
                    distance=9999
                    #print sys.exc_info()
                return distance 
            
            def search_apa(search_radius):
                #print search_radius
                return data_pre[data_pre.loc[:,'lat_long'].apply(lambda x: great_circle_distance(x)<search_radius)]

            
            #print target_location_coords
            
            data=search_apa(float(radius_input))
            #print radius_input
            #print data[['mapaddress','where']].head(10)
            
            data_html=data[['price','attr_space','attr_type','chinese_content','datetime','mapaddress','where','name','url']]
            data_html.rename(columns={'price': 'asking_price', 'attr_space': 'Space', 'attr_type':'Type','datetime':'Post_time','where':'City','name':'headline'}, inplace=True)
            data_html=data_html[data_html['Type'].notnull()]
            def suggest_price(x):
                import random
                try:
                    return '${:,.2f}'.format(float(str(x)[1:])+random.uniform(-300, 300))
                except:
                    return 'NAN'
            
            data_html['suggest_price']=data_html['asking_price'].apply(lambda x: suggest_price(x))
            data_html= data_html[['asking_price','suggest_price','Space','Type','Post_time','City','headline','url']]

            apa_studio=data_html[data_html['Type'].str.contains('0BR')].head(5)
            apa_1BR=data_html[data_html['Type'].str.contains('1BR')].head(5)
            apa_2BR=data_html[data_html['Type'].str.contains('2BR')].head(5)
            apa_3BR=data_html[data_html['Type'].str.contains('3BR')].head(5)
            
            #print target_location_coords
            
            return render_template('view.html',tables=[apa_studio.to_html(classes='apa_studio',escape=False),\
                                                  apa_1BR.to_html(classes='apa_1BR',escape=False),\
                                                  apa_2BR.to_html(classes='apa_2BR',escape=False),\
                                                  apa_3BR.to_html(classes='apa_3BR',escape=False)],\
                               titles = ['Nearby apartments', 'Top 5: Studio','Top 5: 1 Bedroom','Top 5: 2 Bedroom','Top 5: 3 Bedroom']\
                              ,radius_input=radius_input, print_address=print_address   )
        else:
            return redirect('/error_page')


@app.route('/error_page', methods=['GET', 'POST'])
def error_page():
    return render_template('error_page.html')


if __name__ == '__main__':
     app.run(host='0.0.0.0')