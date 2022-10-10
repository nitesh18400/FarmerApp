import json
import os

import pandas as pd
from FarmerApp.settings import GOOGLE_API_KEY
from google.cloud import translate_v2 as translate
from rest_framework import status

from .models import Farmer, HindiFarmerDetails, MarathiFarmerDetails, TeleguFarmerDetails, PunjabiFarmerDetail

lang_list = ["hi", "mr", "pa", "te"]
language_dict = {
    "Hindi": "hi",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Telugu": "te",
    "English": "en",
}


def translate_text(text, target_list):
    json.dump(GOOGLE_API_KEY, open("key.json", 'w'))

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    translate_client = translate.Client()

    result = {}
    for target in target_list:
        result[target] = translate_client.translate(text, source_language="en", target_language=target)[
            "translatedText"].split(",")

    os.remove("key.json")

    return result


def save_farmer(file):
    try:
        df = pd.read_csv(file)
        if list(df.columns) != ['phone_number', 'farmer_name', 'state_name', 'district_name', 'village_name']:
            return {"status": False,
                    "message": "Headers should be like ['phone_number', 'farmer_name', 'state_name', 'district_name', 'village_name']"}

    except:
        return {"status": False, "message": "Uploaded File is not Supported."}

    for _, farmer in df.iterrows():
        farmer_object = Farmer(name=farmer.farmer_name,
                               village_name=farmer.village_name,
                               district_name=farmer.village_name,
                               state_name=farmer.state_name,
                               phone_number=farmer.phone_number)
        farmer_object.save()
        other_lang_data = translate_text(
            text=f"{farmer.farmer_name},{farmer.village_name},{farmer.village_name},{farmer.state_name}",
            target_list=lang_list)

        HindiFarmerDetails(farmer=farmer_object,
                           name=other_lang_data["hi"][0],
                           village_name=other_lang_data["hi"][1],
                           district_name=other_lang_data["hi"][2],
                           state_name=other_lang_data["hi"][3]).save()

        MarathiFarmerDetails(farmer=farmer_object,
                             name=other_lang_data["mr"][0],
                             village_name=other_lang_data["mr"][1],
                             district_name=other_lang_data["mr"][2],
                             state_name=other_lang_data["mr"][3]).save()

        TeleguFarmerDetails(farmer=farmer_object,
                            name=other_lang_data["te"][0],
                            village_name=other_lang_data["te"][1],
                            district_name=other_lang_data["te"][2],
                            state_name=other_lang_data["te"][3]).save()

        PunjabiFarmerDetail(farmer=farmer_object,
                            name=other_lang_data["pa"][0],
                            village_name=other_lang_data["pa"][1],
                            district_name=other_lang_data["pa"][2],
                            state_name=other_lang_data["pa"][3]).save()


def extract_info(request):
    if "lang" not in request.GET:
        return {"status": status.HTTP_400_BAD_REQUEST,
                "message": f"Please Enter Language Code {language_dict} as a GET Parameter --> base_url/info/?lang = language code"}

    if "lang" in request.GET:
        if request.GET["lang"] not in language_dict.values():
            return {"status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Please Enter Valid Language Code {language_dict} as a GET Parameter --> base_url/info/?lang = language code"}
        else:
            lang = request.GET["lang"]

    info = []
    all_farmer = Farmer.objects.all()
    if lang == "hi":
        all_farmer = HindiFarmerDetails.objects.all()
    elif lang == "mr":
        all_farmer = MarathiFarmerDetails.objects.all()
    elif lang == "te":
        all_farmer = TeleguFarmerDetails.objects.all()
    elif lang == "pa":
        all_farmer = PunjabiFarmerDetail.objects.all()

    for farmer in all_farmer:
        info.append({"name": farmer.name,
                     "village_name": farmer.village_name,
                     "district_name": farmer.district_name,
                     "state_name": farmer.state_name,
                     "phone_number": farmer.get_phone_number()})

    return {"status": status.HTTP_200_OK, "message": info}
