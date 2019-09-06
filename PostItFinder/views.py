from django.shortcuts import render
from django.conf import settings
import os
from json import load

def index(request):
    with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
        CONFIG = load(f)["HTML"]
        
    context = {"title": CONFIG["TITLE_TEXT"],
               "body_text": CONFIG["BODY_TEXT"]}
    return render(request, "PostItFinder/index.html", context=context)
