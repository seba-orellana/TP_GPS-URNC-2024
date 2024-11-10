import pandas as pd
import folium

Latitude = []
Longitude = []

with open('TP_GPS-URNC-2024\gps_2024.txt') as file:
    for line in file:
        if line.startswith('$GPGGA'): 

            a = float(line.split(",")[2])/100
            #aaaa.bbbb
            b = ((a - int(a))*100)/60
            a = int(a)
            Latitude.append(-1*(a+b))

            a = float(line.split(",")[4])/100
            #aaaa.bbbb
            b = ((a - int(a))*100)/60
            a = int(a)
            Longitude.append(-1*(a+b))

data = {
    'Latitude': Latitude,
    'Longitude': Longitude
}

df = pd.DataFrame(data)

mymap = folium.Map( location=[ df.Latitude.mean(), df.Longitude.mean() ], zoom_start=14)

for coord in df[['Latitude','Longitude']].values:
    folium.CircleMarker(location=[coord[0],coord[1]], radius=1,color='red').add_to(mymap)

mymap.save('gps_unrc.html') 