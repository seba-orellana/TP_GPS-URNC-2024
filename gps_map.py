#Estadisticas y estructura de datos
import pandas as pd
#Graficador de puntos en mapa
import folium
#Box con metricas en pantalla
from branca.element import Template, MacroElement
#Conversion de formato de segundos a HH:MM:SS
import datetime
#Calculo de distancias entre puntos
import geopy.distance

Latitud = []
Longitud = []
Tiempo = []

#$GPGGA,143809.000,3306.5977,S,06418.1914,W,1,07,1.3,428.9,M,21.4,M,,0000*5D

with open('gps12_11_24_2.txt') as file:
    for line in file:
        if line.startswith('$GPGGA'): 

            a = float(line.split(",")[2])/100
            #aaaa.bbbb
            b = ((a - int(a))*100)/60
            a = int(a)
            Latitud.append(-1*(a+b))

            a = float(line.split(",")[4])/100
            #aaaa.bbbb
            b = ((a - int(a))*100)/60
            a = int(a)
            Longitud.append(-1*(a+b))

            a = float(line.split(",")[1])
            Tiempo.append(a)

data = {
    'Latitud': Latitud,
    'Longitud': Longitud,
    'Tiempo': Tiempo
}

tiempo_total= datetime.timedelta(seconds=(data['Tiempo'][-1] - data['Tiempo'][0]))

df = pd.DataFrame(data)

distancia_total = 0
for i in range(len(df[['Latitud','Longitud']].values)-1):
    coord1 = (df['Latitud'].values[i], df['Longitud'].values[i])
    coord2 = (df['Latitud'].values[i+1], df['Longitud'].values[i+1])
    distancia_total += float(str(geopy.distance.distance(coord1, coord2)*1000).replace(" km",""))

distancia_total = round(distancia_total, 2)

mymap = folium.Map( location=[ df.Latitud.mean(), df.Longitud.mean() ], zoom_start=14)

for coord in df[['Latitud','Longitud']].values:
    folium.CircleMarker(location=[coord[0],coord[1]], radius=1,color='red').add_to(mymap)

folium.CircleMarker(location=df[['Latitud','Longitud']].values[0], radius=7,color='blue').add_child(folium.Popup('Inicio del recorrido')).add_to(mymap)
folium.CircleMarker(location=df[['Latitud','Longitud']].values[-1], radius=7,color='blue').add_child(folium.Popup('Fin del recorrido')).add_to(mymap)

#Metricas de interes dentro de CSS

textbox_css = """
{{% macro html(this, kwargs) %}}
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>GPS 2024 - Radionavegacion</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer"/>
    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>

    <script>
      $( function() {{
        $( "#textbox" ).draggable({{
          start: function (event, ui) {{
            $(this).css({{
              right: "auto",
              top: "auto",
              bottom: "auto"
            }});
          }}
        }});
      }});
    </script>
  </head>

  <body>
    <div id="textbox" class="textbox">
      <div class="textbox-title">Metricas Medidas:</div>
      <div class="textbox-content">
        <p>Tiempo total del recorrido: {tiempo_total}</p>
        <p>Distancia total del recorrido: {distancia_total} metros</p>
      </div>
    </div>
 
</body>
</html>

<style type='text/css'>
  .textbox {{
    position: absolute;
    z-index:9999;
    border-radius:4px;
    background: rgba( 28, 25, 56, 0.75 );
    box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
    backdrop-filter: blur( 4px );
    -webkit-backdrop-filter: blur( 4px );
    border: 4px solid rgba( 215, 164, 93, 0.2 );
    padding: 10px;
    font-size:14px;
    right: 20px;
    bottom: 20px;
    color: orange;
  }}
  .textbox .textbox-title {{
    color: darkorange;
    text-align: center;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 22px;
    }}
</style>
{{% endmacro %}}
""".format(tiempo_total=str(tiempo_total), distancia_total=str(distancia_total))
# configuring the custom style (you can call it whatever you want)
my_custom_style = MacroElement()
my_custom_style._template = Template(textbox_css)

# Adding my_custom_style to the map
mymap.get_root().add_child(my_custom_style)

# Adding the layer control
folium.LayerControl(collapsed=False).add_to(mymap)

mymap.save('gps_unrc121124_a.html') 