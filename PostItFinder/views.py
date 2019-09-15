from django.shortcuts import render
from django.conf import settings
import os
from json import load

from PostItFinder.forms import UploadImageForm

def index(request):
    # NOTE: can I replace these with the built-in static finders?
    with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
        CONFIG = load(f)["HTML"]
        
    form = UploadImageForm(label_suffix='')
    # check if input is HTTP POST   
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES, label_suffix='')
        if form.is_valid():
            # if the form is valid, then do something(not yet sure what...)
            # see https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/ 
            print("Form is valid")
        else:
            # there are errors in the form; print to terminal 
            print(form.errors)

    context = {"title": CONFIG["TITLE_TEXT"],
               "body_text": CONFIG["BODY"]["TEXT"],
               "form": form,
               "submit_id": CONFIG["UPLOAD_IMG_FORM"]["UPLOAD_IMG_BTN"]["ID"],
               "submit_text": CONFIG["UPLOAD_IMG_FORM"]["UPLOAD_IMG_BTN"]["TEXT"]}

    return render(request, "PostItFinder/index.html", context=context)   
    