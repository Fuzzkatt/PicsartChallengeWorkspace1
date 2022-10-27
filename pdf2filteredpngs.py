import requests
import json
import argparse
import fitz
from PIL import Image
import os

parser = argparse.ArgumentParser()
parser.add_argument('pdf_file')
parser.add_argument('--adjust', default=False, action="store_true")
args = parser.parse_args()

doc = fitz.open(args.pdf_file)

images = []
new_pdf_file = f"{args.pdf_file[:-4]}_fixed.pdf"

# for each page in the pdf
for i in range(len(doc)):
    print(f"working on page {i+1} of {len(doc)}...")
    
    # store page as temporary png files
    page = doc[i]
    pix = page.get_pixmap(dpi=288)
    png_file = f"{args.pdf_file[:-4]}_page{i+1}.png"
    pix.save(png_file)

    # do optional adjusts
    if args.adjust:
        url = "https://api.picsart.io/tools/demo/adjust"
        payload={"contrast": "100", "brightness": "0", "saturation": "0", "sharpen": "100", "shadows": "0", "clarity": "100", "temperature": "0", "format": "PNG", "hue": "0", "vignette": "0", "noise": "0", "highlights": "0"}
        files=[('image',(png_file, open(png_file, 'rb'),'image/png'))]
        headers = {"accept": "application/json", "apikey": "sifH0Y0MoRLcboeYh899RiWFw29vt0Pz"}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        data = json.loads(response.text)
        url = data['data']['url']
        img_data = requests.get(url).content
        with open(png_file, 'wb') as handler:
            handler.write(img_data)
    
    # do mandatory upscale
    url = "https://api.picsart.io/tools/demo/upscale/enhance"
    payload={"unit": "px", "format": "PNG", "upscale_factor": "2"}
    files=[('image',(png_file, open(png_file, 'rb'),'image/png'))]
    headers = {"accept": "application/json", "apikey": "sifH0Y0MoRLcboeYh899RiWFw29vt0Pz"}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    data = json.loads(response.text)
    url = data['data']['url']
    img_data = requests.get(url).content
    with open(png_file, 'wb') as handler:
        handler.write(img_data)
    
    # store final result
    png = Image.open(png_file).convert("RGB")
    images.append(png)

# merge resultant pngs into result pdf
images[0].convert("RGB").save(new_pdf_file, resolution=100.0, save_all=True, append_images=images[1:])

# remove temporary png files
# files_to_remove = f"{args.pdf_file[:-4]}_page*"
# os.system(f"rm {files_to_remove}")
