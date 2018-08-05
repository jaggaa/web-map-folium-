import webbrowser
import folium
import os
import pandas

fig = folium.Figure()
fig.html.add_child(folium.Element("<h1>This is a title</h1>"))
m = folium.Map(location=[20,20])
fig.add_child(m)
fig.save("mymap.html")

data = pandas.read_csv("Volcanoes_USA.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
# print(lat)


def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"


# list of coordinates(where to center the map), object of Map class
mymap = folium.Map(location=[25, 81], zoom_start=6, width="100%", tiles="Mapbox Bright",
                   attr="Enter some text here")   # layer 1


fgp = folium.FeatureGroup(name="Population")     # layer 2
fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
                             style_function=lambda x: {"fillColor": "green" if x["properties"]["POP2005"] < 10000000
                             else "orange" if x["properties"]["POP2005"] < 20000000 else "red"}))


fgv = folium.FeatureGroup(name="Volcanoes")       # layer 3
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=str(el)+" m", radius=6, fill_color=color_producer(el),
                                      color="grey", fill_opacity=0.7, fill=True))

mymap.add_child(fgp)        # adding featuregroup(child) object to mymap(parent) object
mymap.add_child(fgv)

mymap.add_child(folium.LayerControl())

mymap.save("Map1.html")
webbrowser.open("file://" + os.path.realpath("Map1.html"))   # to automatically open the map

