
import imp
import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import folium
from folium import plugins
from numpy import true_divide
import rioxarray as rxr
import earthpy as et
import earthpy.spatial as es
import matplotlib.pyplot as plt
import webbrowser
import pandas as pd
from IPython.display import display
from folium.plugins import MarkerCluster
from folium import IFrame
from folium_jsbutton import JsButton
import geopandas
import overpy
import time


class getMap:
    def __init__(self):
        # Import data from EarthPy
        self.data = et.data.get_data('colorado-flood')

        # Set working directory to earth-analytics
        #os.chdir(os.path.join(et.io.HOME, 'earth-analytics', 'data'))

    def getmap():
        path = "veri/20_202106_guzergah.csv"
        databus = pd.read_csv(path, sep=";")

        databus.ENLEM = databus.ENLEM.str.replace(".", "")

        databus.BOYLAM = databus.BOYLAM.str.replace(".", "")

        databus.ENLEM = databus.ENLEM.astype(float)
        databus.BOYLAM = databus.BOYLAM.astype(float)

        databus.ENLEM = databus.ENLEM/1000000
        databus.BOYLAM = databus.BOYLAM/1000000

        path2 = "veri/38_202103_trafik_isik.csv"
        df2 = pd.read_csv(path2)
        df2 = df2.loc[df2.DURUM != "Yesil Dalga"]
        df2 = df2.reset_index(drop=True)

        trafic_lights = []
        for point in range(len(df2)):
            trafic_lights.append([df2["ENLEM"][point], df2["BOYLAM"][point]])

        # Import data from EarthPy
        data = et.data.get_data('colorado-flood')

        # Set working directory to earth-analytics
        #os.chdir(os.path.join(et.io.HOME, 'earth-analytics', 'data'))

        m = folium.Map(location=[37.881853, 32.489888],
                       tiles='cartodbpositron', zoom_start=16, control_scale=True)

        # hava kalitesini ölçen noktaların harita kontrolcüsü
        markers = folium.FeatureGroup(
            name="Hava Kalitesi Kontrol Noktaları", show=False).add_to(m)

        # trafik ışıklarını kontrol eden noktaların kontrolcüsü
        trafik_isik = folium.FeatureGroup(
            name="Trafik Işık Noktaları", show=False).add_to(m)

        # otobüs güzergah hattını temsil eden kontrolcü
        trafic_line = folium.FeatureGroup(
            name="Otobüs Güzergah Hattı", show=False).add_to(m)

        okul_areas = folium.FeatureGroup(name="Okullar", show=False).add_to(m)

        bike_areas = folium.FeatureGroup(
            name="Bisiklet Yolları", show=False) .add_to(m)

        path_okul = "veri/okullar.geojson"
        okul = geopandas.read_file(path_okul)
        folium.GeoJson(data=okul["geometry"]).add_to(okul_areas)
        # add_to(okul_areas)-failed for now
        #okul_path = "veri/okullar.geojson"
        # okul=geopandas.read_file(okul_path)
        # folium.GeoJson(data=okul["geometry"]).add_to(okul_areas)
        # print(okul.geometry[0])

        # Add marker for Boulder, CO
        # folium.Marker(
        #    location=[37.871540, 32.498914], # coordinates for the marker
        #    popup='Earth Lab at CU Boulder', # pop-up label for the marker
        #    icon=folium.Icon() ).add_to(m)

        for num in databus.ANA_HAT_NO.unique():
            databus1 = databus.loc[databus.ANA_HAT_NO == num]
            databus1 = databus1.reset_index(drop=True)
            kord = []
            for point in range(len(databus1)):
                kord.append(
                    tuple([databus1.ENLEM[point], databus1.BOYLAM[point]]))
            folium.PolyLine(kord, opacity=0.06,
                            color="#942C68").add_to(trafic_line)

        # for light in trafic_lights:
         #   folium.Marker(location=light, # coordinates for the marker
          #      popup='Trafik Işık', # pop-up label for the marker
           #         icon=folium.Icon(icon='map-pin', prefix='fa',icon_size=0.1, icon_color="red") ).add_to(m)

        # for point in range(0,len(databus1),15):
        #    folium.Marker(location=[databus1.ENLEM[point], databus1.BOYLAM[point]], # coordinates for the marker
         #                               popup='Earth Lab at CU Boulder', # pop-up label for the marker
          #                              icon=folium.Icon() ).add_to(m)

        tileLayerrr = folium.FeatureGroup(
            name="Görünüm-2", show=False).add_to(m)
        folium.TileLayer('openstreetmap').add_to(tileLayerrr)

        havaDegerler = [40.71, 25.78, 77.99, 29.97,
                        29.47, 45.84, 68.49, 0, 20.37, 16.09]
        #renkler =["", "orange", "lightblue", "pink","green" ,"purple","darkgreen", "red","black" ]

        def AgacOneri(havaKiri):
            text = "PM10 değeri: " + str(havaKiri) + "\n"
            if(havaKiri > 65):
                return text + "Hava Tehlike Seviyesi: 5\n Önerilen Bitki Türü: Ladin"
            elif(havaKiri > 50):
                return text + "Hava Tehlike Seviyesi: 4\n Önerilen Bitki Türü: Kayın Ağacı"
            elif(havaKiri > 35):
                return text + "Hava Tehlike Seviyesi: 3\n Önerilen Bitki Türü: Meşe"
            elif(havaKiri > 25):
                return text + "Hava Tehlike Seviyesi: 2\n Önerilen Bitki Türü: Çam"
            elif(havaKiri > 15):
                return text + "Hava Tehlike Seviyesi: 1\n Önerilen Bitki Türü: Şimşir"
            else:
                return "Eksik veri sorunu"

        folium.Marker(location=[37.870010, 32.517043], tooltip="Karatay 1 Ölçüm Noktası",
                      popup=AgacOneri(havaDegerler[0]),
                      icon=folium.Icon(color="green", icon='building ', prefix='fa')).add_to(markers)

        folium.Circle(
            radius=1500,
            location=[37.870010, 32.517043],
            color='green', weight=2,
            fill=True, opacity=0.6).add_to(markers)

        folium.Marker(location=[37.844698, 32.513969], tooltip="Karatay 2 Ölçüm Noktası",
                      popup=AgacOneri(havaDegerler[1]),
                      icon=folium.Icon(color="red", icon='building ', prefix='fa')).add_to(markers)

        folium.Circle(
            radius=1500,
            location=[37.844698, 32.513969],
            color='red', weight=2,
            fill=True, opacity=0.6).add_to(markers)

        folium.Marker(location=[37.917843, 32.505660], tooltip="Selçuklu Ölçüm Noktası",
                      popup=AgacOneri(havaDegerler[2]),
                      icon=folium.Icon(color="black", icon='building ', prefix='fa')).add_to(markers)

        folium.Circle(
            radius=1500,
            location=[37.917843, 32.505660],
            color='black', weight=2,
            fill=True, opacity=0.6).add_to(markers)

        folium.Marker(location=[38.013184, 32.520520], tooltip="Bosna Ölçüm Noktası",
                      ppopup=AgacOneri(havaDegerler[3]),
                      icon=folium.Icon(color="gray", icon='building ', prefix='fa')).add_to(markers)

        folium.Circle(
            radius=1500,
            location=[38.013184, 32.520520],
            color='gray', weight=2,
            fill=True, opacity=0.6).add_to(markers)

        folium.Marker(location=[37.860659, 32.470254], tooltip="Meram Ölçüm Noktası",
                      popup=AgacOneri(havaDegerler[4]),
                      icon=folium.Icon(color="orange", icon='building ', prefix='fa')).add_to(markers)

        folium.Circle(
            radius=1500,
            location=[37.860659, 32.470254],
            color='orange', weight=2,
            fill=True, opacity=0.6).add_to(markers)

        folium.Marker(location=[37.907138, 32.459662], tooltip="Erenköy Ölçüm Noktası",
                      popup=AgacOneri(havaDegerler[5]),
                      icon=folium.Icon(color="darkgreen", icon='building ', prefix='fa')).add_to(markers)

        folium.Circle(
            radius=1500,
            location=[37.907138, 32.459662],
            color='darkgreen', weight=2,
            fill=True, opacity=0.6).add_to(markers)

        folium.Marker(location=[37.903952, 32.527440], tooltip="Karkent Ölçüm Noktası",
                      popup=AgacOneri(havaDegerler[6]),
                      icon=folium.Icon(color="beige", icon='building ', prefix='fa')).add_to(markers)

        folium.Circle(
            radius=1500,
            location=[37.903952, 32.527440],
            color='beige', weight=2,
            fill=True, opacity=0.6).add_to(markers)

        folium.Marker(location=[37.883034, 32.485458], tooltip="Merkez Trafik Ölçüm Noktası",
                      popup=AgacOneri(havaDegerler[7]),
                      icon=folium.Icon(color="purple", icon='building ', prefix='fa')).add_to(markers)

        folium.Circle(
            radius=1500,
            location=[37.883034, 32.485458],
            color='purple', weight=2,
            fill=True, opacity=0.6).add_to(markers)

        folium.Marker(location=[38.357237, 31.419943], tooltip="Akşehir Ölçüm Noktası",
                      popup=AgacOneri(havaDegerler[8]),
                      icon=folium.Icon(color="lightblue", icon='building ', prefix='fa')).add_to(markers)

        folium.Circle(
            radius=3000,
            location=[38.357237, 31.419943],
            color='lightblue', weight=2,
            fill=True, opacity=0.6).add_to(markers)

        folium.Marker(location=[38.514783, 32.459111], tooltip="Sarayönü Ölçüm Noktası",
                      popup=AgacOneri(havaDegerler[9]),
                      icon=folium.Icon(color="pink", icon='building ', prefix='fa')).add_to(markers)

        folium.Circle(
            radius=2500,
            location=[38.514783, 32.459111],
            color='pink', weight=2,
            fill=True, opacity=0.6).add_to(markers)

        marker_cluster = MarkerCluster(trafic_lights, overlay=True)

        # YENİ ALAN

        mobeseSille = folium.FeatureGroup(
            name="mobeseSille", show=False).add_to(m)
        folium.Marker(location=[37.881853, 32.489888],
                      icon=folium.Icon(color="red", icon='warning ', prefix='fa')).add_to(mobeseSille)

        normalYol = folium.FeatureGroup(name="normalYol").add_to(m)
        normalKoord = ((37.891476, 32.497210), (37.887738, 32.495195), (37.884545, 32.491740), (37.880899, 32.488906),
                       (37.879452, 32.487855))
        folium.PolyLine(normalKoord).add_to(normalYol)

        altYol = folium.FeatureGroup(name="altYol", show=False).add_to(m)
        altKoord = ((37.888341, 32.495430), (37.887774, 32.495054), (37.888358, 32.493831), (37.887367, 32.493069), (37.886454, 32.492594), (37.885248, 32.491175),
                    (37.884854, 32.490637), (37.883766, 32.489772), (37.883476, 32.489862), (37.882333, 32.489039))
        folium.PolyLine(altKoord).add_to(altYol)

        sayac=0
        kaza_durumu=True
        def kaza():
            normalYol.show=False
            altYol.show=True
            mobeseSille.show=True
            JsButton(
                    title='<i class="fas fa-crosshairs"></i>', function="""
    					function(btn, map) {
    						map.setView([37.871540, 32.498914],12);
    						btn.state('zoom-to-forest');
    					}
    					""").add_to(m)

            JsButton(

                    title='<i class="fas fa-book"></i>', function="""
    					function(btn, map) {
    						print()
    					}
    					""").add_to(m)



        def normal():
            JsButton(
                    title='<i class="fas fa-crosshairs"></i>', function="""
    					function(btn, map) {
    						map.setView([37.871540, 33.498914],12);
    						btn.state('zoom-to-forest');
    					}
    					""").add_to(m)

            JsButton(

                    title='<i class="fas fa-book"></i>', function="""
    					function(btn, map) {
    						print()
    					}
    					""").add_to(m)

        if kaza_durumu:
            kaza()
        else:
            normal()


        scheduler = BackgroundScheduler()
        running_job = scheduler.add_job(normal, 'interval', seconds=15, max_instances=1)
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())


        kaza_durumu = False

        def kaza():
            normalYol.show = False
            altYol.show = True
            mobeseSille.show = True
            JsButton(
                title='<i class="fas fa-crosshairs"></i>', function="""
                        function(btn, map) {
                            map.setView([37.871540, 32.498914],12);
                            btn.state('zoom-to-forest');
                        }
                        """).add_to(m)
            JsButton(
                title='<i class="fas fa-book"></i>', function="""
                        function(btn, map) {
                            print()
                        }
                        """).add_to(m)

        def normal():
            JsButton(
                title='<i class="fas fa-crosshairs"></i>', function="""
                        function(btn, map) {
                            map.setView([37.871540, 33.498914],12);
                            btn.state('zoom-to-forest');
                        }
                        """).add_to(m)
            JsButton(
                title='<i class="fas fa-book"></i>', function="""
                        function(btn, map) {
                            print()
                        }
                        """).add_to(m)
        if kaza_durumu:
            kaza()
        else:
            normal()
        # Add marker cluster to map
        marker_cluster.add_to(trafik_isik)
        folium.LayerControl().add_to(m)
        return m
