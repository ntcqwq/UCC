from bs4 import BeautifulSoup
from colr import color

# A html-python color-converter for text-image.com made by Noah (@SSnipro) :D

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def pct(file_path):
    textImage = ""
    soup = BeautifulSoup(open(file_path), 'html.parser')
    pixelRows = soup.prettify().split("\n")
    for pixelRow in pixelRows:
        pixel = pixelRow.split("<")
        prow = ""
        for eachPixel in pixel:
            if "b style=" in eachPixel:
                pixelColor = eachPixel.split(">")[0].split(":")[1].replace('"',"")
                pixelText = eachPixel.split(">")[1].replace("0","█").replace("1","█")
                prow += color(pixelText, fore=hex_to_rgb(pixelColor))
        textImage += f"{prow}\n"
    return textImage