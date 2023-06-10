#!/usr/bin/env python
# coding: utf-8




import folium
import geopandas as gpd
from folium.plugins import MarkerCluster
import webbrowser
import PySimpleGUI as sg
import numpy as np
from scipy.spatial import distance
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import json
from urllib.request import urlopen
from datetime import datetime,timedelta

#計算起點與終點之間的最短路徑距離
'''
import osmnx as ox
import networkx as nx

def get_distance(start_x,start_y,end_x,end_y):
    G = ox.graph_from_point((start_y,start_x), dist=100000 ,network_type='all')
    origin = ox.get_nearest_node(G, (start_y,start_x))
    destination = ox.get_nearest_node(G, (end_y,end_x))
    length=nx.shortest_path_length(G, origin, destination)
    return length
G = ox.graph_from_point((22.967120,120.208234), dist=30000 ,network_type='all')
G = ox.project_graph(G)
ox.plot_graph(G)
origin = ox.nearest_nodes(G, 22.995696,120.218135)
destination = ox.nearest_nodes(G, 23.012957,120.183521)
route = nx.shortest_path(G, origin, destination)
ox.plot_graph_route(G, route)
length=nx.shortest_path_length(G, origin, destination,weight='length')
print(length)
'''

gdf1=gpd.read_file("convenience_store.geojson")
gdf1_list = [[point.xy[1][0], point.xy[0][0]] for point in gdf1.geometry]
gdf1_tuple = [(point.xy[1][0], point.xy[0][0]) for point in gdf1.geometry]
map = folium.Map(location=[23.012332, 120.184106], tiles="OpenStreetMap", zoom_start=12)
mCluster = MarkerCluster(name="convenientstores").add_to(map)
for coordinates in gdf1_list:#convenient store location
     # Place the markers with the popup labels and data
    mCluster.add_child(
        folium.Marker(
            location=coordinates,
            popup="經度:{} 緯度:{}".format(coordinates[1],coordinates[0]),
            icon=folium.Icon(icon='shop',prefix='fa',color="red")
        )
    )

gdf2=gpd.read_file("Taiwan_cycle_network.geojson")
gdf2=folium.GeoJson(data=gdf2.geometry) #cycle network
gdf2.add_to(map)
folium.LayerControl().add_to(map)
map.save('map.html')

sg.theme('LightBrown1')
layout=[[sg.Text('輸入預估速度的資料集:')],
        [sg.Text('距離 (公里):'),sg.Input(key='-distance-'),sg.Text('時間 (分鐘):'),sg.Input(key='-time-')],
        [sg.Button('增加'),sg.Button('清除前一個資料'),sg.Button('清除資料集')],
        [sg.Text('')],
        [sg.Text('出發地 緯度:'),sg.Input(key='-start1-'),sg.Text('出發地 經度:'),sg.Input(key='-start2-')],
        [sg.Text('目的地 緯度:'),sg.Input(key='-end1-'),sg.Text('目的地 經度:'),sg.Input(key='-end2-')],
        [sg.Button('確認')],
        [sg.Text(key='-output1-')],
        [sg.Text(key='-output2-')],
        [sg.Text('大概的體重(60以下打50，60~70打60，70~80打70，80~90打80，90以上打90):'),sg.Input(key='-kg-')],
        [sg.Text('去程總公里數:'),sg.Input(key='-dis-')],
        [sg.Text('預估到達時間 202x-xx-xx xx:xx (若是是某一天的日出、日落時間請打 202x-xx-xx 日出/日落 ) :'),sg.Input(key='-dest_time-')],
        [sg.Text('會經過的縣市 (可複選)')],
        [sg.Button('基隆市'),sg.Button('臺北市'),sg.Button('新北市'),sg.Button('桃園市'),sg.Button('新竹縣'),
        sg.Button('新竹市'),sg.Button('苗栗縣'),sg.Button('臺中市'),sg.Button('彰化縣'),sg.Button('雲林縣'),sg.Button('南投縣')],
        [sg.Button('嘉義縣'),sg.Button('嘉義市'),sg.Button('臺南市'),sg.Button('高雄市'),sg.Button('屏東縣'),
        sg.Button('臺東縣'),sg.Button('花蓮縣'),sg.Button('宜蘭縣'),sg.Button('澎湖縣'),sg.Button('金門縣'),sg.Button('連江縣')],
        [sg.Text('賞日出、日落的縣市')],
        [sg.Button('基隆市',key='基隆市1'),sg.Button('臺北市',key='臺北市1'),sg.Button('新北市',key='新北市1'),sg.Button('桃園市',key='桃園市1'),sg.Button('新竹縣',key='新竹縣1'),
        sg.Button('新竹市',key='新竹市1'),sg.Button('苗栗縣',key='苗栗縣1'),sg.Button('臺中市',key='臺中市1'),sg.Button('彰化縣',key='彰化縣1'),sg.Button('雲林縣',key='雲林縣1'),sg.Button('南投縣',key='南投縣1')],
        [sg.Button('嘉義縣',key='嘉義縣1'),sg.Button('嘉義市',key='嘉義市1'),sg.Button('臺南市',key='臺南市1'),sg.Button('高雄市',key='高雄市1'),sg.Button('屏東縣',key='屏東縣1'),
        sg.Button('臺東縣',key='臺東縣1'),sg.Button('花蓮縣',key='花蓮縣1'),sg.Button('宜蘭縣',key='宜蘭縣1'),sg.Button('澎湖縣',key='澎湖縣1'),sg.Button('金門縣',key='金門縣1'),sg.Button('連江縣',key='連江縣1')],
        [sg.Button('計算'),sg.Text('(每按完一次計算若要再計算必須再按一次上面的縣市按鈕)')],
        [sg.Text(key='-output3-')],
        [sg.Text(key='-output4-')],
        [sg.Text(key='-output5-')],
        [sg.Text(key='-output6-')],
        [sg.Button('台灣的自行車道和便利商店 (補給點) 地點'),sg.Button('台灣的自行車道和便利商店 (補給點) 地點結合出發地和目的地'),sg.Push(),sg.Button('Exit')]
]
window=sg.Window('cycling app',layout,size=(1200,700 ))

sunrise_sunset_url='https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/A-B0062-001?Authorization=rdec-key-123-45678-011121314&format=JSON'
weather_url='https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-005?Authorization=rdec-key-123-45678-011121314&format=JSON'

sunrise_sunset_open = urlopen(sunrise_sunset_url)
sunrise_sunset_json = json.loads(sunrise_sunset_open.read())

weather_open = urlopen(weather_url)
weather_json = json.loads(weather_open.read())

sunrise_sunset_list=[]
weather_list=[]
rain_list=[]

calorie={'50':[100,210,315],'60':[120,252,378],'70':[140,294,441],'80':[160,336,504],'90':[180,378,567]}

s=""

while True:
    event,values=window.read()
  
    if event=='Exit' or event==sg.WIN_CLOSED:
        break
    if event=='台灣的自行車道和便利商店 (補給點) 地點':
        webbrowser.open('map.html', new=2) #show map on website
    if event=='增加':
        data = pd.read_csv("cycle_distance_and_time.csv")
        distance1=data['distance'].tolist()
        distance1.append(float(values['-distance-']))
        time1=data['time'].tolist()
        time1.append(float(values['-time-']))
        df = pd.DataFrame({'distance':distance1, 'time':time1})
        df.to_csv('cycle_distance_and_time.csv')
    if event=='清除前一個資料':
        data = pd.read_csv("cycle_distance_and_time.csv")
        distance1=data['distance'].tolist()
        distance1.pop()
        time1=data['time'].tolist()
        time1.pop()
        df = pd.DataFrame({'distance':distance1, 'time':time1})
        df.to_csv('cycle_distance_and_time.csv')
    if event=='清除資料集':
        df = pd.DataFrame({'distance':[], 'time':[]})
        df.to_csv('cycle_distance_and_time.csv')
    if event=='確認':
        start=(float(values['-start1-']),float(values['-start2-']))
        destination=(float(values['-end1-']),float(values['-end2-']))
        distances1 = distance.cdist([start], gdf1_tuple, 'euclidean')
        nearest_point_index1 = np.argmin(distances1)
        nearest_point1 = gdf1_list[nearest_point_index1]
        window['-output1-'].Update('離出發地最近的便利商店位置 : ( 緯度:{} , 經度:{} )'.format(nearest_point1[0],nearest_point1[1]))
        distances2 = distance.cdist([destination], gdf1_tuple, 'euclidean')
        nearest_point_index2 = np.argmin(distances2)
        nearest_point2 = gdf1_list[nearest_point_index2]
        window['-output2-'].Update('離目的地最近的便利商店位置 : ( 緯度:{} , 經度:{} )'.format(nearest_point2[0],nearest_point2[1]))
    if event=='台灣的自行車道和便利商店 (補給點) 地點結合出發地和目的地':
        map2=map
        folium.Marker(location=[values['-start1-'], values['-start2-']],
                      popup='出發地',
                     icon=folium.Icon(icon='circle-play',prefix='fa',color="darkgreen")).add_to(map2)
        folium.Marker(location=[values['-end1-'], values['-end2-']],
                      popup='目的地',
                     icon=folium.Icon(icon='flag',prefix='fa',color="green")).add_to(map2)
        folium.Marker(location=[nearest_point1[0], nearest_point1[1]],
                      popup='離出發地最近的便利商店',
                     icon=folium.Icon(icon='shop',prefix='fa',color="darkred")).add_to(map2)
        folium.Marker(location=[nearest_point2[0], nearest_point2[1]],
                      popup='離目的地最近的便利商店',
                     icon=folium.Icon(icon='shop',prefix='fa',color="lightred")).add_to(map2)
        map2.save("map2.html")
        webbrowser.open("map2.html", new=2)
    if event=='基隆市':
        weather_list.append('基隆市')
    if event=='臺北市':
        weather_list.append('臺北市')
    if event=='新北市':
        weather_list.append('新北市')
    if event=='桃園市':
        weather_list.append('桃園市')
    if event=='新竹縣':
        weather_list.append('新竹縣')
    if event=='新竹市':
        weather_list.append('新竹市')
    if event=='苗栗縣':
        weather_list.append('苗栗縣')
    if event=='臺中市':
        weather_list.append('臺中市')
    if event=='彰化縣':
        weather_list.append('彰化縣')
    if event=='雲林縣':
        weather_list.append('雲林縣')
    if event=='南投縣':
        weather_list.append('南投縣')
    if event=='嘉義縣':
        weather_list.append('嘉義縣')
    if event=='嘉義市':
        weather_list.append('嘉義市')
    if event=='臺南市':
        weather_list.append('臺南市')
    if event=='高雄市':
        weather_list.append('高雄市')
    if event=='屏東縣':
        weather_list.append('屏東縣')
    if event=='臺東縣':
        weather_list.append('臺東縣')
    if event=='花蓮縣':
        weather_list.append('花蓮縣')
    if event=='宜蘭縣':
        weather_list.append('宜蘭縣')
    if event=='澎湖縣':
        weather_list.append('澎湖縣')
    if event=='金門縣':
        weather_list.append('金門縣')
    if event=='連江縣':
        weather_list.append('連江縣')
    if event=='基隆市1':
        sunrise_sunset_list.append('基隆市')
    if event=='臺北市1':
        sunrise_sunset_list.append('臺北市')
    if event=='新北市1':
        sunrise_sunset_list.append('新北市')
    if event=='桃園市1':
        sunrise_sunset_list.append('桃園市')
    if event=='新竹縣1':
        sunrise_sunset_list.append('新竹縣')
    if event=='新竹市1':
        sunrise_sunset_list.append('新竹市')
    if event=='苗栗縣1':
        sunrise_sunset_list.append('苗栗縣')
    if event=='臺中市1':
        sunrise_sunset_list.append('臺中市')
    if event=='彰化縣1':
        sunrise_sunset_list.append('彰化縣')
    if event=='雲林縣1':
        sunrise_sunset_list.append('雲林縣')
    if event=='南投縣1':
        sunrise_sunset_list.append('南投縣')
    if event=='嘉義縣1':
        sunrise_sunset_list.append('嘉義縣')
    if event=='嘉義市1':
        sunrise_sunset_list.append('嘉義市')
    if event=='臺南市1':
        sunrise_sunset_list.append('臺南市')
    if event=='高雄市1':
        sunrise_sunset_list.append('高雄市')
    if event=='屏東縣1':
        sunrise_sunset_list.append('屏東縣')
    if event=='臺東縣1':
        sunrise_sunset_list.append('臺東縣')
    if event=='花蓮縣1':
        sunrise_sunset_list.append('花蓮縣')
    if event=='宜蘭縣1':
        sunrise_sunset_list.append('宜蘭縣')
    if event=='澎湖縣1':
        sunrise_sunset_list.append('澎湖縣')
    if event=='金門縣1':
        sunrise_sunset_list.append('金門縣')
    if event=='連江縣1':
        sunrise_sunset_list.append('連江縣')
    if event=='計算':
        
        dataset = pd.read_csv("cycle_distance_and_time.csv")
        X = dataset.iloc[:,1].values.reshape(-1,1)
        Y = dataset.iloc[:,2].values
        regress = LinearRegression()
        regress.fit(X, Y)
        time_pred = regress.predict([[float(values['-dis-'])]])
        
        plt.scatter(X, Y, color = 'red')
        plt.plot(X, regress.predict(X), color = 'blue')
        plt.title('Predict Time Model')
        plt.xlabel("distance(km)")
        plt.ylabel("time(minute)")
        plt.grid(True)
        
        
        time_100=regress.predict([[100]])
        speed=100/(time_100[0]/60)
        window['-output3-'].Update('速度為 {} 公里/小時，去程需要 {} 分鐘'.format(speed,time_pred[0]))
        if(speed<20):
            heat=calorie[values['-kg-']][0]*(time_pred[0]/30)
        elif(speed>=20 and speed<30):
            heat=calorie[values['-kg-']][1]*(time_pred[0]/30)
        else:
            heat=calorie[values['-kg-']][2]*(time_pred[0]/30)
        window['-output4-'].Update('共會消耗 {} 卡路里'.format(heat))
        
        
        if values['-dest_time-'][-2:]=="日出" or values['-dest_time-'][-2:]=="日落":
            for i in sunrise_sunset_json["cwbopendata"]["dataset"]['location']:
                if i["CountyName"]==sunrise_sunset_list[0]:
                    for j in i["time"]:
                        if j["Date"]==values['-dest_time-'][0:10]:
                            if values['-dest_time-'][-2:]=="日出":
                                day_time=values['-dest_time-'][0:10]+" "+j["SunRiseTime"]
                            if values['-dest_time-'][-2:]=="日落":
                                day_time=values['-dest_time-'][0:10]+" "+j["SunSetTime"]
        else:
            day_time=values['-dest_time-']
        day_time_time = datetime.strptime(day_time, '%Y-%m-%d %H:%M')
        day_time_time2=day_time_time-timedelta(minutes = int(time_pred[0]))
        if values['-dest_time-'][-2:]=="日出" or values['-dest_time-'][-2:]=="日落":
            window['-output5-'].Update('{}在 {}，建議在 {} 出發'.format(values['-dest_time-'][-2:],day_time,str(day_time_time2)))
        else:
            window['-output5-'].Update('建議在 {} 出發'.format(str(day_time_time2)))
        
        
        for k in weather_list:
            for z in weather_json["cwbopendata"]["dataset"]["location"]:
                if z["locationName"]==k:
                    for m in z["weatherElement"]:
                        if m["elementName"]=="Wx":
                            for n in m["time"]:
                                weather_time=(n["startTime"][0:10])+" "+(n["startTime"][11:19])
                                weather_time=datetime.strptime(weather_time, '%Y-%m-%d %H:%M:%S')
                                weather_time_end=(n["endTime"][0:10])+" "+(n["endTime"][11:19])
                                weather_time_end=datetime.strptime(weather_time_end, '%Y-%m-%d %H:%M:%S')
                                print((weather_time-day_time_time).total_seconds())
                                print((weather_time-day_time_time2).total_seconds())
                                if ((weather_time-day_time_time).total_seconds()<0 and (weather_time-day_time_time2).total_seconds()>0) or ((weather_time_end-day_time_time).total_seconds()>0 and (weather_time-day_time_time2).total_seconds()<0):
                                    for x in n["parameter"]["parameterName"]:
                                        if x=="雨" and k not in rain_list:
                                            rain_list.append(k)
        print(rain_list)                                    
        for l in rain_list:
            if s=="":
                s=l
            else:
                s=s+"、"+l
        if s=="":
            window['-output6-'].Update("天氣晴朗，直接開騎")
        else:
            window['-output6-'].Update("{}有雨，建議延期".format(s))
        
        plt.show()
        sunrise_sunset_list=[]
        weather_list=[]
        rain_list=[]
        s=""
       
if os.path.exists("map2.html"):
    os.remove("map2.html")      
map2=map    
window.close()







