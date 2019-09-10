from django import forms
from django.conf import settings

import os
from json import load

with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
        CONFIG = load(f)["HTML"]["UPLOAD_IMAGE_FORM"]

class UploadImageForm(forms.Form):
    choose_img_btn = forms.ImageField(label=CONFIG["CHOOSE_IMAGE_LBL"]["TEXT"])