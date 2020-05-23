import xml.etree.ElementTree as ET
import matplotlib.pyplot as PLT
import requests
import helpers

def fetch_and_plot_data(year, fmisid):
    url = "http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature"
    storedquery_id = "fmi::observations::weather::daily::simple"
    starttime = str(year)+"-01-01T00:00:00Z"
    endtime = str(year)+"-12-31T00:00:00Z"
    fmisid = str(fmisid)
    parameters = "tmin"

    url = "{}&storedquery_id={}&starttime={}&endtime={}&parameters={}&fmisid={}".format(url, storedquery_id, starttime, endtime, parameters, fmisid)

    response = requests.get(url)
    data = ET.fromstring(response.text)

    temp = []

    for child in data:
        temp.append(float(child[0][3].text))
    
    PLT.plot(temp, marker="o", linestyle = 'None', alpha=.2, color='white', label=year)

def plot_range(name, startYear, endYear, fmisid):
    print("Downloading weather data from fmi.fi...")

    progress = '░'
    y = int(startYear)
    while y <= int(endYear):
        helpers.clear()
        print("Fetching weather data from fmi.fi for: ")
        print(name)
        print(str(y)+"/"+str(endYear)+" "+progress)
        fetch_and_plot_data(y, fmisid)
        y += 1
        progress += '░'

    helpers.seperator()
    print("Rendering chart...")

# Matplotlib
PLT.style.use('dark_background')
PLT.title('Temperatures over the years')
PLT.xlabel('January to December')
PLT.ylabel('Temperature')
PLT.box(False)
PLT.grid()

# CLI
# Runs plot_range(name, startYear, endYear, fmisid) e.g. plot_range(Inari, 2014, 2018, 102017)

presets = {
    102016: 'Enontekiö Kilpisjärvi 102016 (Halti Trail, Käsivarren Wilderness Area)',
    102026: 'Inari Angeli Lintupuoliselkä 102026 (Lemmenjoki National Park & Muotkatunturi Wilderness Area)',
    102019: 'Enontekiö Näkkälä 102019 (Tarvantovaara & Pöyrisjärvi Wilderness Area)',
    102009: 'Inari Raja-Jooseppi 102009 (Urho Kekkonen National Park)',
}

def render_menu():
    print("Finnish Meteorological Stations v1.0.0")
    print("Chart temperature data from multiple years.")
    helpers.seperator()

    position = 1
    for value in presets.values():
        print(str(position)+") "+value)
        position += 1

    print("0) Other")
    helpers.seperator()

def menu_preset(name,fmisid):
    helpers.clear()
    print(name)
    helpers.seperator()
    fromYear = input("From (year): ")
    toYear = input("To (year): ")
    helpers.seperator()

    plot_range(name, fromYear, toYear, fmisid)

def menu_logic():
    # helpers.seperator()
    choice = input("Choose menu option:")

    position = 1
    for fmisid, value in presets.items():
        if choice == str(position):
            menu_preset(value, fmisid)
        position += 1

    if choice == "0":
        helpers.clear()
        print("List of weather stations: " + "https://en.ilmatieteenlaitos.fi/observation-stations")

        helpers.seperator()
        fmisid = input("Weather station ID: ")
        fromYear = input("From (year): ")
        toYear = input("To (year): ")
        helpers.seperator()

        plot_range(fmisid, fromYear, toYear, fmisid)

# Render menu on app start
helpers.clear()
render_menu()
menu_logic()

# Display chart
PLT.show()