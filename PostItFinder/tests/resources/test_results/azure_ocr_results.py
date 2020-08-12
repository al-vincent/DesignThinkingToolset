# ================================================================================================
# Name: azure_ocr_results.py
# Description: fixtures-type file providing a series of JSON-style dict objects for testing the 
# TextAnalyser class in azure_services.py. Used by test_azure_ocr_services.py.
# 
# This was preferable to constructing the same dicts in code (e.g. by popping keys, reassigning 
# list vals etc.), as an error could be made when using code to achieve the same thing.
# ================================================================================================

# ------------------------------------------------------------------------------------------------
# AZURE OCR RAW RESULTS
# ------------------------------------------------------------------------------------------------
# This dict represents the OCR results when run against test.jpg.jpg. 
# All the dicts below are derived by editing this.
OCR_RESULTS = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"boundingBox": [1679,1441,2446,1382,2458,1679,1686,1711],
								"text": "WORDS",
								"confidence": 0.981
							}
						]
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": [
							{
								"boundingBox": [2119,1923,2756,1810,2774,2016,2148,2114],
								"text": "HERE",
								"confidence": 0.985
							}
						]
					}
				]
			}
		]
	}
}

OCR_NO_ANALYZERESULT_KEY = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z"
}

OCR_NO_READRESULTS_KEY = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0"		
	}
}

OCR_READRESULTS_EMPTY_LIST = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": []
	}
}

OCR_NO_LINES_KEY = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel"
			}
		]
	}
}

OCR_NO_WIDTH_KEY = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"boundingBox": [1679,1441,2446,1382,2458,1679,1686,1711],
								"text": "WORDS",
								"confidence": 0.981
							}
						]
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": [
							{
								"boundingBox": [2119,1923,2756,1810,2774,2016,2148,2114],
								"text": "HERE",
								"confidence": 0.985
							}
						]
					}
				]
			}
		]
	}
}

OCR_NO_HEIGHT_KEY = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"boundingBox": [1679,1441,2446,1382,2458,1679,1686,1711],
								"text": "WORDS",
								"confidence": 0.981
							}
						]
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": [
							{
								"boundingBox": [2119,1923,2756,1810,2774,2016,2148,2114],
								"text": "HERE",
								"confidence": 0.985
							}
						]
					}
				]
			}
		]
	}
}

OCR_LINES_EMPTY_LIST = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": []
			}
		]
	}
}

OCR_NO_WORDS_KEYS= {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS"					
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE"
					}
				]
			}
		]
	}
}

OCR_ALL_WORDS_EMPTY_LISTS = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": []
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": []
					}
				]
			}
		]
	}
}

OCR_ONE_WORDS_KEY = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"boundingBox": [1679,1441,2446,1382,2458,1679,1686,1711],
								"text": "WORDS",
								"confidence": 0.981
							}
						]
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE"						
					}
				]
			}
		]
	}
}

OCR_ONE_WORDS_LIST = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"boundingBox": [1679,1441,2446,1382,2458,1679,1686,1711],
								"text": "WORDS",
								"confidence": 0.981
							}
						]
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": []
					}
				]
			}
		]
	}
}

# NOTE: for this test-case, we *DO* want 'boundingBox' keys in 'lines' - just not 
# in 'words'
OCR_NO_BOUNDINGBOX_KEYS = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"text": "WORDS",
								"confidence": 0.981
							}
						]
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": [
							{
								"text": "HERE",
								"confidence": 0.985
							}
						]
					}
				]
			}
		]
	}
}

OCR_ONE_BOUNDINGBOX_KEY = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"boundingBox": [1679,1441,2446,1382,2458,1679,1686,1711],
								"text": "WORDS",
								"confidence": 0.981
							}
						]
					},
					{
                        "boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": [
							{							
								"text": "HERE",
								"confidence": 0.985
							}
						]
					}
				]
			}
		]
	}
}

# NOTE: for this test-case, we *DO* want 'text' keys in 'lines' - just not in 'words'
OCR_NO_TEXT_KEYS_IN_WORDS = { 
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"boundingBox": [1679,1441,2446,1382,2458,1679,1686,1711],
								"confidence": 0.981
							}
						]
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": [
							{
								"boundingBox": [2119,1923,2756,1810,2774,2016,2148,2114],
								"confidence": 0.985
							}
						]
					}
				]
			}
		]
	}
}

OCR_ONE_TEXT_KEY_IN_WORDS = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"boundingBox": [1679,1441,2446,1382,2458,1679,1686,1711],
								"text": "WORDS",
								"confidence": 0.981
							}
						]
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": [
							{
								"boundingBox": [2119,1923,2756,1810,2774,2016,2148,2114],
								"confidence": 0.985
							}
						]
					}
				]
			}
		]
	}
}

OCR_NO_CONFIDENCE_KEYS = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"boundingBox": [1679,1441,2446,1382,2458,1679,1686,1711],
								"text": "WORDS"
							}
						]
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": [
							{
								"boundingBox": [2119,1923,2756,1810,2774,2016,2148,2114],
								"text": "HERE"
							}
						]
					}
				]
			}
		]
	}
}

OCR_ONE_CONFIDENCE_KEY = {
	"status": "succeeded",
	"createdDateTime": "2020-08-03T12:15:02Z",
	"lastUpdatedDateTime": "2020-08-03T12:15:04Z",
	"analyzeResult": {
		"version": "3.0.0",
		"readResults": [
			{
				"page": 1,
				"angle": -3.0396,
				"width": 4608,
				"height": 3456,
				"unit": "pixel",
				"lines": [
					{
						"boundingBox": [1574,1437,2457,1381,2469,1673,1581,1711],
						"text": "WORDS",
						"words": [
							{
								"boundingBox": [1679,1441,2446,1382,2458,1679,1686,1711],
								"text": "WORDS",
								"confidence": 0.981
							}
						]
					},
					{
						"boundingBox": [2057,1922,2761,1808,2782,2008,2089,2121],
						"text": "HERE",
						"words": [
							{
								"boundingBox": [2119,1923,2756,1810,2774,2016,2148,2114],
								"text": "HERE",
							}
						]
					}
				]
			}
		]
	}
}

# ------------------------------------------------------------------------------------------------
# AZURE OCR PROCESSED RESULTS
# ------------------------------------------------------------------------------------------------
PROCESSED_OCR_RESULTS = [
	{
		'x': 0.3643663194444444, 
		'y': 0.39988425925925924, 
		'width': 0.16905381944444445, 
		'height': 0.09519675925925926, 
		'text': 'WORDS', 
		'confidence': 0.981
	}, 
	{
		'x': 0.4598524305555556, 
		'y': 0.5237268518518519, 
		'width': 0.1421440972222222, 
		'height': 0.08796296296296297, 
		'text': 'HERE', 
		'confidence': 0.985
	}
]

PROCESSED_OCR_ONE_WORD = [
	{
		'x': 0.3643663194444444, 
		'y': 0.39988425925925924, 
		'width': 0.16905381944444445, 
		'height': 0.09519675925925926, 
		'text': 'WORDS', 
		'confidence': 0.981
	}
]

PROCESSED_OCR_NO_CONFIDENCE_KEYS = [
	{
		'x': 0.3643663194444444, 
		'y': 0.39988425925925924, 
		'width': 0.16905381944444445, 
		'height': 0.09519675925925926, 
		'text': 'WORDS', 
		'confidence': None
	}, 
	{
		'x': 0.4598524305555556, 
		'y': 0.5237268518518519, 
		'width': 0.1421440972222222, 
		'height': 0.08796296296296297, 
		'text': 'HERE', 
		'confidence': None
	}
]

PROCESSED_OCR_ONE_CONFIDENCE_KEY = [
	{
		'x': 0.3643663194444444, 
		'y': 0.39988425925925924, 
		'width': 0.16905381944444445, 
		'height': 0.09519675925925926, 
		'text': 'WORDS', 
		'confidence': 0.981
	}, 
	{
		'x': 0.4598524305555556, 
		'y': 0.5237268518518519, 
		'width': 0.1421440972222222, 
		'height': 0.08796296296296297, 
		'text': 'HERE', 
		'confidence': None
	}
]