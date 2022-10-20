import requests
import json
import argparse
import fitz
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument('pdf_file')
args = parser.parse_args()

doc = fitz.open(args.pdf_file)

images = []
new_pdf_file = f"{args.pdf_file[:-4]}_fixed.pdf"

for i in range(len(doc)):
    print(f"working on page {i+1} of {len(doc)}...")
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
    url = data['data']['url']

    img_data = requests.get(url).content
    with open(png_file, 'wb') as handler:
        handler.write(img_data)

    png = Image.open(png_file).convert("RGB")
    images.append(png)

images[0].convert("RGB").save(new_pdf_file, resolution=100.0, save_all=True, append_images=images[1:])

