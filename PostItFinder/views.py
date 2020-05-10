from django.shortcuts import render
from django.conf import settings
from django.urls import reverse

import os
from json import load


# NOTE: can I replace these with the built-in static finders?
with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
    CONFIG = load(f)
    PATHS = CONFIG["PATHS"]
    HTML = CONFIG["HTML"]

def index(request):
    # Update config to include the explanatory text for the home page

    HTML["APP"]["EXPLAIN_TEXT"]["TEXT"] =  HTML["HOME"]["EXPLAIN_TEXT"]["TEXT"]
    HTML["APP"]["STEPPER_BAR"]["ITEMS"][0]["CLASS"] = "active"

    # Update URL for the 'next' button
    HTML["APP"]["NEXT_BTN"]["URL"] = HTML["HOME"]["NEXT_BTN"]["URL"]

    context = {
        "title": HTML["TITLE"],
        "navbar": HTML["BASE"]["NAVBAR"],
        "stepper": HTML["APP"]["STEPPER_BAR"],
        "explain_text": HTML["APP"]["EXPLAIN_TEXT"],
        "next_btn": HTML["APP"]["NEXT_BTN"],
        "prev_btn": HTML["APP"]["PREVIOUS_BTN"],
        "choose_img_btn": HTML["HOME"]["CHOOSE_IMG_BTN"],
        "image_pane": HTML["APP"]["IMAGE_PANE"],
        "config": CONFIG,
        }

    return render(request, PATHS["HOME"], context=context)

def about(request):
    context = {
        "title": "About",
        "about_content": "some info about the app"
        }
    
    return render(request, PATHS["ABOUT"], context=context)

def faq(request):
    context = {
        "title": "FAQ",
        "faq_content": "some frequently asked questions"
        }
    
    return render(request, PATHS["FAQ"], context=context)

def set_regions(request):
    context = {
        "title": "Set Regions",
        "navbar": HTML["BASE"]["NAVBAR"],
        "stepper": HTML["APP"]["STEPPER_BAR"],
        "explain_text": HTML["APP"]["EXPLAIN_TEXT"],
        "next_btn": HTML["APP"]["NEXT_BTN"],
        "prev_btn": HTML["APP"]["PREVIOUS_BTN"],
        "choose_img_btn": HTML["HOME"]["CHOOSE_IMG_BTN"],
        "image_pane": HTML["APP"]["IMAGE_PANE"],
        }

    return render(request, PATHS["SET_REGIONS"], context=context)