### Scrapes the KSRSAC site to generate polling station boundary GeoJSONs. Dumped GeoJSONs represent the response from square tiles of size 2000x2000

# TODO: Cleanup/Refactor this script

from urllib.parse import quote_plus
import time
import subprocess

# Lowest X co-ordinate for Karnataka
x = 8240000.069888774

for i in range(0, 300):
    # Lowest Y co-ordinate for Karnataka
    y = 1290000.9393397346

    # Scrape in steps of squares with 2000x2000 size
    x = x + 2000

    for j in range(0, 400):
        # Scrape in steps of squares with 2000x2000 size
        y = y + 2000

        # Form the geometry part of the request URL
        geometry = '{"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":' + str(x) + ',"ymin":' + str(y) + ',"xmax":' + str(x + 2000) + ',"ymax":' + str(y + 2000) + '}'

        other_params = '&orderByFields=OBJECTID%20ASC&outFields=*&outSR=4326&quantizationParameters='

        # Form the quantization part of the request URL
        quantization = '{"extent":{"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":' + str(x) + ',"ymin":' + str(y) + ',"xmax":' + str(x + 2000) + ',"ymax":' + str(y + 2000) + '},"mode":"view","originPosition":"upperLeft","tolerance":2.388657133911135}'

        # URL Encode the geometry part of the URL
        geometry_encode = quote_plus(geometry)

        # URL Encode the quantization part of the URL
        quantization_encode = quote_plus(quantization)

        # Form the complete query request URL
        request = 'https://kgis.ksrsac.in/kgismaps1/rest/services/Polling/AC_Boundary/MapServer/1/query?f=geojson&geometry=' + geometry_encode + other_params + quantization_encode + '&resultType=tile&returnCentroid=true&returnExceededLimitFeatures=false&spatialRel=esriSpatialRelIntersects&where=1%3D1&geometryType=esriGeometryEnvelope&inSR=102100'

        # Print the curl request being made to the console
        print("curl '" + request + "' -H 'Accept: */*' -H 'Referer: https://kgis.ksrsac.in/pollinginfo/' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' > karnataka" + str(i) + '_' + str(j) + '.geojson')

        # Make the curl request and save the response to a geojson file
        subprocess.getoutput("curl '" + request + "' -H 'Accept: */*' -H 'Referer: https://kgis.ksrsac.in/pollinginfo/' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' > karnataka" + str(i) + '_' + str(j) + '.geojson')

        # Take a 1 second break between successive scrape requests
        time.sleep(1)
