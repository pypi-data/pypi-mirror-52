#%%
"""
    Upload Ecel catalog, still firebase v1 database format
"""

#%% Import Module
import pandas as pd
import os
import datetime
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from larisinpy import utcnow
from larisinpy.connection import FirebaseUtils

import logging
from larisinpy.connection import FirebaseRealtime
#%%
logging = logging.getLogger(__name__)

#%%
FB_CREDENTIALS_PATH = "creds/larisin-prod-firebase.json"
FB_DB_URL="https://larisin-v2.firebaseio.com/"


#%% Class
class SKUUploader(object):
    
    def __init__(self, df):
        
        df["barcode"] = df["barcode"].astype(str)
        df["ratio"] = df["ratio"].astype(int)
        
        self.df = df
        self.df = self.df.fillna("N/A")
        self.entity_id = self.df["store_code"][0]

        self.ACCESS_KEY = "creds/larisin-prod.json"
        self.DB_PATH = "https://larisin-v2.firebaseio.com/"

    def _check_barcode_exist(self, barcode):

        # Checking Barcode exist or not
        path = "/catalog/wholesaler/{}/{}".format(self.entity_id, barcode)
        ref = db.reference(path)
        result = ref.get()

        if result is None:
            return False
        else:
            return True

    def _check_uom_exist(self, barcode, uom):

        # Checking UOM exist or not
        path = "/catalog/wholesaler/{}/{}/uom/{}".format(
            self.entity_id, barcode, uom
        )
        ref = db.reference(path)
        result = ref.get()

        if result is None:
            return False
        else:
            return True

    def _check_min_order_exist(self, barcode, uom, min_order):

        # Checking MinOrder exist or not
        path = "/catalog/wholesaler/{}/{}/uom/{}/minOrder/{}".format(
            self.entity_id, barcode, uom, min_order
        )
        ref = db.reference(path)
        result = ref.get()

        if result is None:
            return False
        else:
            return True

    def _check_minus_one_uom(self, barcode):

        # Checking -1 exist or not
        path = "/catalog/wholesaler/{}/{}/uom/-1".format(
            self.entity_id, barcode
        )

        ref = db.reference(path)
        result = ref.get()

        if result != "":
            return False
        else:
            return True

    def add(self):

        fr = FirebaseRealtime(FB_CREDENTIALS_PATH, FB_DB_URL)
        app = fr.connect()

        path = "/catalog/wholesaler"

        for index in self.df.index:

            barcode = self.df["barcode"][index]
            if (barcode != "N/A") and (self.df["status"][index] == "UPLOAD_ALL"):

                # Check is barcode exist
                is_barcode_exist = self._check_barcode_exist(barcode)
                if is_barcode_exist:   
                        
                    # Check is uom exist
                    is_uom_exist = self._check_uom_exist(
                                        barcode, self.df["ratio"][index]
                                    )

                    if not is_uom_exist:
                        ref = db.reference(path + "/{}/{}".format(
                                self.entity_id, barcode))

                        data = ref.get()
                        data["uom"].update({
                            str(self.df["ratio"][index]):{
                                "cog" : int(self.df["cogs"][index]),
                                "s"   : int(self.df["stock"][index]),
                                "lbl" : str(self.df["unit"][index]),
                                "oty" : int(self.df["order_type"][index]),
                                "min" : {
                                    "-1":"",
                                    "1": {
                                        "p1": float(self.df["normal_price"][index]),
                                        "p2": float(self.df["bronze_price"][index]),
                                        "p3": float(self.df["silver_price"][index]),
                                        "p4": float(self.df["gold_price"][index])   
                                    }
                                }
                            }
                        })

                        ref.set(data)

                        self.df["status"][index] = "SUCCESS_UPLOADED_SKU"
                        self.df["checked_time"][index] = str(datetime.datetime.now())

                    else:
                        logging.warning("""Ratio '{} dan Unit {} pada Barcode {} sudah""" 
                                        """ada, silahkan gunakan fitur Update.""".format(
                                        self.df["ratio"][index], 
                                        self.df["unit"][index], 
                                        barcode))
                        
                        self.df["status"][index] = "FAILED_ALREADY_UPLOADED"
                        self.df["checked_time"][index] = str(datetime.datetime.now())

                else:
                    
                    ref = db.reference(path + "/{}/{}".format(
                        self.entity_id, barcode)
                    )

                    data = {
                        "uom":{
                            "-1":"",
                            str(self.df["ratio"][index]):{
                                "cog":int(self.df["cogs"][index]),
                                "s"  :int(self.df["stock"][index]),
                                "lbl":str(self.df["unit"][index]),
                                "oty":int(self.df["order_type"][index]),
                                "min" : {
                                    "-1":"",
                                    "1": {
                                        "p1": float(self.df["normal_price"][index]),
                                        "p2": float(self.df["bronze_price"][index]),
                                        "p3": float(self.df["silver_price"][index]),
                                        "p4": float(self.df["gold_price"][index])   
                                        }
                                    }
                                }
                        },
                        "pnm" : "",
                        "isk" : str(self.df["sku"][index]),
                        "inm" : str(self.df["product_name"][index]), 
                        "cat" : str(self.df["category"][index]),
                        "dsc" : "",
                        "c"   : utcnow(),
                        "u"   : utcnow()
                    }

                    ref.set(data)
                    
                    self.df["status"][index] = "SUCCESS_UPLOADED_SKU"
                    self.df["checked_time"][index] = str(datetime.datetime.now())

        logging.warning('Done.')
        fr.disconnect(app)

    def update_all(self):

        fr = FirebaseRealtime(FB_CREDENTIALS_PATH, FB_DB_URL)
        app = fr.connect()

        path = "/catalog/wholesaler"

        for index in self.df.index:

            barcode = self.df["barcode"][index]
            if (barcode != "N/A") and (self.df["status"][index] in ["UPDATE_SKU", "UPDATE_CATEGORY"]):

                # Check is barcode exist
                is_barcode_exist = self._check_barcode_exist(barcode)
                if is_barcode_exist:   
                        
                    # Check is uom exist
                    is_uom_exist = self._check_uom_exist(
                                        barcode, self.df["ratio"][index]
                                    )

                    if is_uom_exist:
                        ref = db.reference(path + "/{}/{}".format(
                                self.entity_id, barcode))

                        data = ref.get()

                        if self.df["status"][index] == "UPDATE_SKU":
                            data["uom"].update({
                                str(self.df["ratio"][index]):{
                                    "cog" : int(self.df["cogs"][index]),
                                    "s"   : int(self.df["stock"][index]),
                                    "lbl" : str(self.df["unit"][index]),
                                    "oty" : int(self.df["order_type"][index]),
                                    "min" : {
                                        "-1":"",
                                        "1": {
                                            "p1": float(self.df["normal_price"][index]),
                                            "p2": float(self.df["bronze_price"][index]),
                                            "p3": float(self.df["silver_price"][index]),
                                            "p4": float(self.df["gold_price"][index])   
                                        }
                                    }
                                }
                            })

                            data.update({
                                "pnm" : "",
                                "isk" : str(self.df["sku"][index]),
                                "inm" : str(self.df["product_name"][index]), 
                                "cat" : str(self.df["category"][index]),
                                "img" : str(self.df["image"][index]),
                                "dsc" : "",
                                "u"   : utcnow()
                            })

                        ref.set(data)

                        self.df["status"][index] = "SUCCESS_UPDATED_SKU"
                        self.df["checked_time"][index] = str(datetime.datetime.now())
                        logging.warning("Updating .. {}".format(barcode))

        logging.warning('Done.')
        fr.disconnect(app)

    def update_category(self):

        fr = FirebaseRealtime(FB_CREDENTIALS_PATH, FB_DB_URL)
        app = fr.connect()

        path = "/catalog/wholesaler"

        for index in self.df.index:

            time.sleep(1)
            barcode = self.df["barcode"][index]
            if (barcode != "N/A") and (self.df["status"][index] == "UPDATE_CATEGORY"):

                # Check is barcode exist
                is_barcode_exist = self._check_barcode_exist(barcode)
                if is_barcode_exist:   
                        
                    # Check is uom exist
                    is_uom_exist = self._check_uom_exist(
                                        barcode, self.df["ratio"][index]
                                    )

                    if is_uom_exist:
                        ref = db.reference(path + "/{}/{}".format(
                                self.entity_id, barcode))

                        data = ref.get()
                        data.update({
                            "cat" : str(self.df["category"][index])
                        })
                        
                        ref.set(data)

                        self.df["status"][index] = "SUCCESS_UPDATED_CATEGORY"
                        self.df["checked_time"][index] = str(datetime.datetime.now())
                        logging.warning("Updating category.. {} as {}".format(
                            barcode, self.df["category"][index]))

            else:
                logging.warning('Skip.. {}, status is {}'.format(
                    barcode, self.df["status"][index]))

        logging.warning('Done.')
        fr.disconnect(app)

    def update_image(self):

        fr = FirebaseRealtime(FB_CREDENTIALS_PATH, FB_DB_URL)
        app = fr.connect()

        path = "/catalog/wholesaler"

        for index in self.df.index:

            time.sleep(1)
            barcode = self.df["barcode"][index]
            if (barcode != "N/A") and (self.df["status"][index] == "UPDATE_IMAGE"):

                # Check is barcode exist
                is_barcode_exist = self._check_barcode_exist(barcode)
                if is_barcode_exist:   
                        
                    # Check is uom exist
                    is_uom_exist = self._check_uom_exist(
                                        barcode, self.df["ratio"][index]
                                    )

                    if is_uom_exist:
                        ref = db.reference(path + "/{}/{}".format(
                                self.entity_id, barcode))

                        data = ref.get()
                        data.update({
                            "img" : str(self.df["image"][index])
                        })
                        
                        ref.set(data)

                        self.df["status"][index] = "SUCCESS_UPDATED_IMAGE"
                        self.df["checked_time"][index] = str(datetime.datetime.now())
                        logging.warning("Updating Image.. {} as {}".format(
                            barcode, self.df["image"][index]))

            else:
                logging.warning('Skip.. {}, status is {}'.format(
                    barcode, self.df["status"][index]))

        logging.warning('Done.')
        fr.disconnect(app)

    
#%%
