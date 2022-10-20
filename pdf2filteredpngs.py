import requests
import json
import argparse
import fitz

parser = argparse.ArgumentParser()
parser.add_argument('pdf_file')
args = parser.parse_args()

doc = fitz.open(args.pdf_file)
for i in range(len(doc)):
    page = doc[i]
    pix = page.get_pixmap()
    png_file = f"{args.pdf_file[:-4]}_page{i+1}.png"
    pix.save(png_file)

    url = "https://api.picsart.io/tools/demo/removebg"

    payload={"bg_blur": "0", "scale": "fit", "format": "PNG", "output_type": "cutout"}
    files=[
        ('image',(png_file, open(png_file, 'rb'),'image/png'))
    ]
    headers = {
        "accept": "application/json", "apikey": "sifH0Y0MoRLcboeYh899RiWFw29vt0Pz"
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    data = json.loads(response.text)
    print(data['data']['url'])
