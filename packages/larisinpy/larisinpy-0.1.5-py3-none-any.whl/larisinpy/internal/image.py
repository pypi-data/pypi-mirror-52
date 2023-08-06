#%%
"""
    Handle Image for internal SKU Uploader
"""
#%%
""" Migration Image from rulo to Google Storage
"""
import pandas as pd
import os
import psycopg2
import time
import urllib.request 
import datetime
from google.cloud import storage
from PIL import Image
import logging

#%%
logging = logging.getLogger(__name__)

#%%
class ImageUploader(object):

    def __init__(self, gcp_credentials, data):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=gcp_credentials
        self.data = data

        if not os.path.exists("image"):
            os.makedirs("image")

    def to_blob(self, image, blob_name, barcode_type):
        """
            Upload to Blob Storage
        """
        storage_client = storage.Client()

        if barcode_type == "principal":
            bucket = storage_client.get_bucket(
                'assets.larisin.id')
            blob = bucket.blob("principal/seller/" + blob_name)

        elif barcode_type == "wholesaler":
            bucket = storage_client.get_bucket(
                'assets.larisin.id')
            blob = bucket.blob("catalog/seller/" + blob_name)

        blob.upload_from_filename(image)
        blob.make_public()

        return blob.public_url

    def download_all(self):
        """
            Download all with Dataframe
        """

        total_data = self.data.shape[0]
        for index in self.data.index:

            time.sleep(3)
            barcode = str(self.data["barcode"][index])
            if self.data["status"][index] == "UPLOAD_IMAGE":

                try:
                    if len(barcode) >= 13 and barcode[:3] != "LRS":
                        barcode_type = "principal"

                        urllib.request.urlretrieve(
                            self.data["image"][index], "image/" + barcode
                        )

                        im = Image.open("image/" + barcode)
                        im.save("image/" + barcode + ".png")

                        image_url = migrate_image_principal(
                            "image/" + barcode + ".png", 
                            barcode + ".png",
                            barcode_type
                        )
                        self.data["image"][index] = image_url

                    elif len(barcode) != 13 or barcode[:3] == "LRS":
                        barcode_type = "wholesaler"

                        urllib.request.urlretrieve(
                            self.data["image"][index], "image/" + barcode
                        )

                        im = Image.open("image/" + barcode)
                        im.save("image/" + barcode + ".png")

                        image_url = migrate_image_principal(
                            "image/" + barcode + ".png", 
                            self.data["store_code"][index] + "/" + barcode + ".png",
                            barcode_type
                        )

                        self.data["image"][index] = image_url

                    os.remove("image/" + barcode)
                    os.remove("image/" + barcode + ".png")

                    self.data["status"][index] = "SUCCESS_UPLOADED_IMAGE"
                    
                except:
                
                    self.data["image"][index] = "CANT_DOWNLOAD : " + self.data["image"][index]
                    self.data["status"][index] = "CANT_DOWNLOAD : " + self.data["image"][index]
                    logging.warning("Cant downloaded: {}".format(barcode))

                self.data["checked_time"][index] = str(datetime.datetime.now())
            
            elif self.data["status"][index] == "N/A":
                logging.warning("Barcode isnt uploaded: {}".format(barcode))

            else:
                logging.warning("Skipped barcode {} with status {}".format(
                    barcode, self.data["status"][index]))

            logging.info("Progress .. {}%".format(int(index/total_data)*100))
            logging.info("Done upload image. With {} total barcode".format(total_data))

            logging.info("Total failed: {}".format(self.data[self.data["status"]=="CANT_DOWNLOAD"].shape[0]))

        return self.data

    def download_one(self, barcode, store_code, filename):
        """
            Download One by One
        """
        if filename[:48] != 'https://storage.googleapis.com/assets.larisin.id':

            try:
                if len(barcode) >= 10 and barcode[:3] != "LRS":
                    barcode_type = "principal"

                    urllib.request.urlretrieve(
                        filename, "image/{}".format(barcode)
                    )

                    im = Image.open("image/{}".format(barcode))
                    im.save("image/{}.png".format(barcode))

                    image_url = self.to_blob(
                        "image/{}.png".format(barcode), 
                        "{}.png".format(barcode),
                        barcode_type
                    )

                elif len(barcode) < 10 or barcode[:3] == "LRS":
                    barcode_type = "wholesaler"

                    urllib.request.urlretrieve(
                        filename, "image/{}".format(barcode)
                    )

                    im = Image.open("image/{}".format(barcode))
                    im.save("image/{}.png".format(barcode))

                    image_url = self.to_blob(
                        "image/{}.png".format(barcode), 
                        "{}/{}.png".format(store_code, barcode),
                        barcode_type
                    )

                os.remove("image/{}".format(barcode))
                os.remove("image/{}.png".format(barcode))
                status = "SUCCESS_UPLOADED_IMAGE"
                    
            except:
                
                image_url = "CANT_DOWNLOAD : {}".format(filename)
                status    = "CANT_DOWNLOAD : {}".format(filename) 
                logging.warning("Cant downloaded: {}".format(barcode))
        else:

            logging.warning("Image already uploaded: {}".format(barcode))
            status = "ALREADY_UPLOADED"
            image_url = filename

        return status, image_url
#%%

