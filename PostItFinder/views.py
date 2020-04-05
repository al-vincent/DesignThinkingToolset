from django.shortcuts import render
from django.conf import settings
import os
from json import load


def index(request):
    # NOTE: can I replace these with the built-in static finders?
    with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
        CONFIG = load(f)["HTML"]

    explain_text = CONFIG["APP"]["EXPLAIN_TEXT"]
    explain_text["TEXT"] =  CONFIG["HOME"]["EXPLAIN_TEXT"]["TEXT"]

    context = {"title": CONFIG["TITLE"],
               "navbar": CONFIG["BASE"]["NAVBAR"],
               "stepper": CONFIG["APP"]["STEPPER_BAR"],
               "explain_text": explain_text,
               "next_btn": CONFIG["APP"]["NEXT_BTN"],
               "prev_btn": CONFIG["APP"]["PREVIOUS_BTN"],
               "choose_img_btn": CONFIG["HOME"]["CHOOSE_IMG_BTN"],
               "image_pane": CONFIG["APP"]["IMAGE_PANE"],
               }

    return render(request, "PostItFinder/index.html", context=context)   
    