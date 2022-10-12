import json
import os
import pandas as pd

from FarmerApp.settings import GOOGLE_API_KEY
from google.cloud import translate_v2 as translate
from rest_framework import status

from .models import Farmer, HindiFarmerDetails, MarathiFarmerDetails, TeleguFarmerDetails, PunjabiFarmerDetail

# Language Conversions List
lang_list = ["hi", "mr", "pa", "te"]

# Language to Code Dictionary
language_dict = {
    "Hindi": "hi",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Telugu": "te",
    "English": "en",
}

# Code to Language Dictionary
code_to_lang = {
    "hi": "Hindi",
    "mr": "Marathi",
    "pa": "Punjabi",
    "te": "Telugu",
    "en": "English",

}


def translate_text(text, target_list):
    # Creation key.json file for environment creation for GOOGLE_APPLICATION_CREDENTIALS
    json.dump(GOOGLE_API_KEY, open("key.json", 'w'))

    # Environment Creation
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

    # Google Translate API Client Initialization
    translate_client = translate.Client()

    result = {}
    # Loop in Different Language code list
    for target in target_list:
        # Get Translated Data from Google API
        result[target] = translate_client.translate(text, source_language="en", target_language=target)[
            "translatedText"].split(",")

    # Removing Key File
    os.remove("key.json")

    return result


def save_farmer(file):
    try:
        # Pandas Read CSV File
        df = pd.read_csv(file)

        # Csv Header Check
        if list(df.columns) != ['phone_number', 'farmer_name', 'state_name', 'district_name', 'village_name']:
            return {"status": False,
                    "message": "Headers should be like ['phone_number', 'farmer_name', 'state_name', 'district_name', 'village_name']"}

    except:
        return {"status": False, "message": "Uploaded File is not Supported."}

    for _, farmer in df.iterrows():
        # Creating Farmer Objects
        farmer_object = Farmer(name=farmer.farmer_name,
                               village_name=farmer.village_name,
                               district_name=farmer.village_name,
                               state_name=farmer.state_name,
                               phone_number=farmer.phone_number)
        # Saving Object
        farmer_object.save()

        # Calling Conversion Function
        other_lang_data = translate_text(
            text=f"{farmer.farmer_name},{farmer.village_name},{farmer.village_name},{farmer.state_name}",
            target_list=lang_list)

        # Saving Hindi Farmer Details
        HindiFarmerDetails(farmer=farmer_object,
                           name=other_lang_data["hi"][0],
                           village_name=other_lang_data["hi"][1],
                           district_name=other_lang_data["hi"][2],
                           state_name=other_lang_data["hi"][3]).save()

        # Saving Marathi Farmer Details
        MarathiFarmerDetails(farmer=farmer_object,
                             name=other_lang_data["mr"][0],
                             village_name=other_lang_data["mr"][1],
                             district_name=other_lang_data["mr"][2],
                             state_name=other_lang_data["mr"][3]).save()

        # Saving Telegu Farmer Details
        TeleguFarmerDetails(farmer=farmer_object,
                            name=other_lang_data["te"][0],
                            village_name=other_lang_data["te"][1],
                            district_name=other_lang_data["te"][2],
                            state_name=other_lang_data["te"][3]).save()

        # Saving Punjabi Farmer Details
        PunjabiFarmerDetail(farmer=farmer_object,
                            name=other_lang_data["pa"][0],
                            village_name=other_lang_data["pa"][1],
                            district_name=other_lang_data["pa"][2],
                            state_name=other_lang_data["pa"][3]).save()


def get_all_farmer_details(lang):

    # Get table object According to Language Code
    if lang == "en":
        all_farmer = Farmer.objects.all()
    elif lang == "hi":
        all_farmer = HindiFarmerDetails.objects.all()
    elif lang == "mr":
        all_farmer = MarathiFarmerDetails.objects.all()
    elif lang == "te":
        all_farmer = TeleguFarmerDetails.objects.all()
    elif lang == "pa":
        all_farmer = PunjabiFarmerDetail.objects.all()

    return all_farmer


def extract_info(request):

    # If code not in request parameter
    if "lang" not in request.GET:
        return {"status": status.HTTP_400_BAD_REQUEST,
                "message": f"Please Enter Language Code {language_dict} as a GET Parameter --> base_url/info/?lang = language code"}

    if "lang" in request.GET:
        # If code in request parameter is wrong
        if request.GET["lang"] not in language_dict.values():
            return {"status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Please Enter Valid Language Code {language_dict} as a GET Parameter --> base_url/info/?lang = language code"}
        else:
            lang = request.GET["lang"]

    info = []

    # Get Details of Farmer From Database according To Lang
    all_farmer = get_all_farmer_details(lang)

    # Creating Response Data Dictionary
    for farmer in all_farmer:
        info.append({"name": farmer.name,
                     "village_name": farmer.village_name,
                     "district_name": farmer.district_name,
                     "state_name": farmer.state_name,
                     "phone_number": farmer.get_phone_number()})

    return {"status": status.HTTP_200_OK, "message": info}
