import requests
import json
import argparse
import fitz
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument('pdf_file')
parser.add_argument('filter')
args = parser.parse_args()

doc = fitz.open(args.pdf_file)

images = []
new_pdf_file = f"{args.pdf_file[:-4]}_fixed.pdf"

for i in range(len(doc)):
    print(f"working on page {i+1} of {len(doc)}...")
    page = doc[i]
    pix = page.get_pixmap(dpi=244)
    png_file = f"{args.pdf_file[:-4]}_page{i+1}.png"
    pix.save(png_file)

    if args.filter == 'upscale':
        url = "https://api.picsart.io/tools/demo/upscale/enhance"
        payload={"unit": "px", "format": "JPG", "upscale_factor": "2"}
    elif args.filter == 'removebg':
        url = "https://api.picsart.io/tools/demo/removebg"
        payload={"bg_blur": "0", "scale": "fit", "format": "PNG", "output_type": "cutout"}
    elif args.filter == 'vectorizer':
        url = "https://api.picsart.io/tools/demo/vectorizer"
        payload={"downscale_to": "2048"}
    elif args.filter == 'adjust':
        url = "https://api.picsart.io/tools/demo/adjust"
        payload={"contrast": "0", "brightness": "0", "saturation": "0", "sharpen": "0", "shadows": "0", "clarity": "0", "temperature": "0", "format": "JPG", "hue": "0", "vignette": "0", "noise": "0", "highlights": "0"}

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

