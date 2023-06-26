# Required packages
# pip install requests
# pip install bs4

# https://www.geeksforgeeks.org/image-scraping-with-python/
import os
import requests
import tkinter as tk # For GUI
from tkinter import filedialog
from bs4 import BeautifulSoup

# TODO:
# - add download path entry
# - add default installation path: downloads
# - create new folder when downloading
# - open new folder after download finishes 

def scrape_prep():
    url = url_var.get()
    # Request directory where to download images
    dirname = filedialog.askdirectory()
    scrape(url, dirname)

def scrape(url, dirname):
    try:
        r = requests.get(url)
        htmldata = r.text
    except:
        tk.messagebox.showerror(title = None, message = 'Invalid URL provided' + url)
        return
    
    # Get image URLs and image names
    images = []
    soup = BeautifulSoup(htmldata, 'html.parser')
    for item in soup.find_all('img'):
        img_url = item['src']
        if img_url:
            img_name = img_url.split('/')[-1]
            img_name = img_name.split('?')[0]
            images.append([img_url, img_name])

    # Download all images into selected directory
    for img in images:
        img_url = img[0]
        img_name = img[1]

        try:
            img_data = requests.get(img_url)
        except:
            tk.messagebox.showwarning(title = None, message = 'Could not download: ' + img_name)
            continue

        download_path = dirname
        os.chdir(download_path)
        
        img_file = open(img_name, "wb")
        img_file.write(img_data.content)
        img_file.close()
    
    print("Successfully downloaded images.")


# Create GUI root window
root = tk.Tk(className = 'image_scrape')
root.geometry('700x80')

url_var = tk.StringVar()
url_label = tk.Label(root, text= 'Website URL', font = ('TkDefaultFont', 10, 'bold'))
url_entry = tk.Entry(root, textvariable = url_var, width = 100)

scrape_btn = tk.Button(root, text = 'Download Images', width = 15, command = scrape_prep)

url_label.pack()
url_entry.pack()
scrape_btn.pack()

root.mainloop()
