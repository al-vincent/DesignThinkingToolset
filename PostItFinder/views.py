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

    # Update config to set the 'active' class for the stepper bar
    for step in HTML["APP"]["STEPPER_BAR"]["ITEMS"]:
        if step["ID"] == "step1-id":
            step["CLASS"] = "active"
        else:
            step["CLASS"] = ""

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
    # Update config to include the explanatory text for the home page
    HTML["APP"]["EXPLAIN_TEXT"]["TEXT"] =  HTML["SET_REGIONS"]["EXPLAIN_TEXT"]["TEXT"]

    # Update config to set the 'active' class for the stepper bar
    for step in HTML["APP"]["STEPPER_BAR"]["ITEMS"]:
        if step["ID"] == "step1-id" or step["ID"] == "step2-id":
            step["CLASS"] = "active"
        else:
            step["CLASS"] = ""

    # Update URL for the 'previous' button
    HTML["APP"]["PREVIOUS_BTN"]["URL"] = HTML["SET_REGIONS"]["PREVIOUS_BTN"]["URL"]

    # Update URL for the 'next' button
    HTML["APP"]["NEXT_BTN"]["URL"] = HTML["SET_REGIONS"]["NEXT_BTN"]["URL"]

    context = {
        "title": "Set Regions",
        "navbar": HTML["BASE"]["NAVBAR"],
        "stepper": HTML["APP"]["STEPPER_BAR"],
        "explain_text": HTML["APP"]["EXPLAIN_TEXT"],
        "next_btn": HTML["APP"]["NEXT_BTN"],
        "prev_btn": HTML["APP"]["PREVIOUS_BTN"],
        "image_pane": HTML["APP"]["IMAGE_PANE"],
        "config": CONFIG,
        }

    return render(request, PATHS["SET_REGIONS"], context=context)

def analyse_text(request):
    context = {
        "title": "Analyse Text",
        "navbar": HTML["BASE"]["NAVBAR"],
        "stepper": HTML["APP"]["STEPPER_BAR"],
        "explain_text": HTML["APP"]["EXPLAIN_TEXT"],
        "next_btn": HTML["APP"]["NEXT_BTN"],
        "prev_btn": HTML["APP"]["PREVIOUS_BTN"],
        "image_pane": HTML["APP"]["IMAGE_PANE"],
        "config": CONFIG,
        }

    return render(request, PATHS["ANALYSE_TEXT"], context=context)
