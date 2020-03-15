from django.shortcuts import render
from django.conf import settings
import os
from json import load

from PostItFinder.forms import UploadImageForm

def index(request):
    # NOTE: can I replace these with the built-in static finders?
    with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
        CONFIG = load(f)["HTML"]
    
    # **********
    # NOTE: this is *MUCH* more oriented towards uploading files to the app server.
    #       I want to upload the file to the Azure server; different process...??
    # **********
    # check if input is HTTP POST  
    img_file = None
    if request.method == 'POST':
        # is POST request; the form has been activated
        form = UploadImageForm(request.POST, request.FILES, label_suffix='')
        if form.is_valid():
            # If the form is valid, I want to:
            # - Show a thumbnail of the image selected
            # useful link: https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/ 
            print("Form is valid")
            print(type(request.FILES["choose_img_btn"]))
            img_file = request.FILES["choose_img_btn"].temporary_file_path()
        else:
            # there are errors in the form; print to terminal 
            print(form.errors)
    else:
        # Not a POST request; just render the form
        form = UploadImageForm(label_suffix='')

    context = {"title": CONFIG["TITLE_TEXT"],
               "body_text": CONFIG["BODY"]["TEXT"],
               "form_id": CONFIG["UPLOAD_IMG_FORM"]["ID"],
               "form": form,
               "submit_id": CONFIG["UPLOAD_IMG_FORM"]["UPLOAD_IMG_BTN"]["ID"],
               "submit_text": CONFIG["UPLOAD_IMG_FORM"]["UPLOAD_IMG_BTN"]["TEXT"],
               "img_file": img_file}

    return render(request, "PostItFinder/index.html", context=context)   
    