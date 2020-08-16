import unittest
import os
from PostItFinder import azure_services
import PostItFinder.tests.resources.test_results.match_words_to_regions_results as RESULTS
from django.conf import settings

# ================================================================================================
# HELPER FUNCTIONS
# ================================================================================================
def get_file_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
    return os.path.join(test_path, "resources", "test_images", file_name)

class TestSubmitImageForProcessing(unittest.TestCase):
    def setUp(self):
        self.image_files = ["match_words_regions_1.jpg"]#, 
                            # "match_words_regions_2.png"], 
                            # "match_words_regions_3.jpg",
                            # "match_words_regions_4.png"]
        self.pred_key = settings.OBJ_DET_PREDICTION_KEY
        self.obj_det_url = settings.OBJ_DET_API_URL
        self.subs_key = settings.OCR_SUBSCRIPTION_KEY
        self.ocr_url = settings.OCR_API_URL
        # self.image_path = get_file_path("test_jpg.jpg")
        # self.img_bytes = azure_services.get_file_bytes(self.image_path)

    def tearDown(self):
        # del(self.image_path, self.img_bytes)
        del(self.image_files, self.pred_key, self.obj_det_url)

    def test_output(self):
        for file in self.image_files:
            image_path = get_file_path(file)
            img_bytes = azure_services.get_file_bytes(image_path)

            print(f"{'='*len(file)}\n{file}\n{'='*len(file)}\n")
            
            # get the regions
            aod = azure_services.ObjectDetector(image_data=img_bytes,
                                                prediction_key=self.pred_key,
                                                obj_det_url=self.obj_det_url)
            regions = aod.analyse_and_process()
            print(f"{'='*7}\nRegions\n{'='*7}\n{regions}")

            # get the text
            ta = azure_services.TextAnalyser(image_data=img_bytes, 
                                            subscription_key=self.subs_key,
                                            api_url=self.ocr_url)
            words = ta.analyse_and_process()
            print(f"{'='*5}\nWords\n{'='*5}\n{words}")

            # match words to regions
            mwtr = azure_services.MatchWordsToRegions(region_data=regions["data"], 
                                                    word_data=words["data"])
            new_regions = mwtr.match()
            print(f"{'='*15}\nRegions & Words\n{'='*15}\n{new_regions}")
            


