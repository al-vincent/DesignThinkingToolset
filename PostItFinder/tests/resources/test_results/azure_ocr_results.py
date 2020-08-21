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

# NOTE: for this test-case, we *DO* want "boundingBox" keys in "lines" - just not 
# in "words"
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

# NOTE: for this test-case, we *DO* want "text" keys in "lines" - just not in "words"
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

# NOTE: this dict is taken from the Microsoft quickstart example, and provides a 
# better test for extracting lines of text. Matches the file lines_of_words.jpg
# Code: https://docs.microsoft.com/en-gb/azure/cognitive-services/computer-vision/quickstarts/python-hand-text
# Original image: https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg 
OCR_TEXT_IN_LINES = {
    "status": "succeeded",
    "createdDateTime": "2020-08-15T13:16:13Z",
    "lastUpdatedDateTime": "2020-08-15T13:16:14Z",
    "analyzeResult": {
        "version": "3.0.0",
        "readResults": [
            {
                "page": 1,
                "angle": 0.6856,
                "width": 2661,
                "height": 1901,
                "unit": "pixel",
                "lines": [
                    {
                        "boundingBox": [
                            38,
                            650,
                            2572,
                            699,
                            2570,
                            854,
                            37,
                            815
                        ],
                        "text": "The quick brown fox jumps",
                        "words": [
                            {
                                "boundingBox": [
                                    116,
                                    654,
                                    478,
                                    672,
                                    477,
                                    819,
                                    115,
                                    818
                                ],
                                "text": "The",
                                "confidence": 0.984
                            },
                            {
                                "boundingBox": [
                                    533,
                                    675,
                                    1005,
                                    692,
                                    1004,
                                    823,
                                    532,
                                    819
                                ],
                                "text": "quick",
                                "confidence": 0.967
                            },
                            {
                                "boundingBox": [
                                    1137,
                                    697,
                                    1620,
                                    707,
                                    1620,
                                    833,
                                    1136,
                                    825
                                ],
                                "text": "brown",
                                "confidence": 0.973
                            },
                            {
                                "boundingBox": [
                                    1653,
                                    707,
                                    2016,
                                    711,
                                    2015,
                                    841,
                                    1653,
                                    833
                                ],
                                "text": "fox",
                                "confidence": 0.559
                            },
                            {
                                "boundingBox": [
                                    2049,
                                    712,
                                    2565,
                                    711,
                                    2565,
                                    854,
                                    2048,
                                    842
                                ],
                                "text": "jumps",
                                "confidence": 0.978
                            }
                        ]
                    },
                    {
                        "boundingBox": [
                            184,
                            1053,
                            508,
                            1044,
                            510,
                            1123,
                            184,
                            1128
                        ],
                        "text": "over",
                        "words": [
                            {
                                "boundingBox": [
                                    221,
                                    1058,
                                    506,
                                    1045,
                                    510,
                                    1125,
                                    221,
                                    1128
                                ],
                                "text": "over",
                                "confidence": 0.835
                            }
                        ]
                    },
                    {
                        "boundingBox": [
                            639,
                            1011,
                            1976,
                            1026,
                            1974,
                            1158,
                            637,
                            1141
                        ],
                        "text": "the lazy dog!",
                        "words": [
                            {
                                "boundingBox": [
                                    669,
                                    1012,
                                    967,
                                    1012,
                                    967,
                                    1144,
                                    668,
                                    1127
                                ],
                                "text": "the",
                                "confidence": 0.985
                            },
                            {
                                "boundingBox": [
                                    1087,
                                    1012,
                                    1504,
                                    1018,
                                    1506,
                                    1158,
                                    1087,
                                    1149
                                ],
                                "text": "lazy",
                                "confidence": 0.981
                            },
                            {
                                "boundingBox": [
                                    1661,
                                    1021,
                                    1974,
                                    1029,
                                    1976,
                                    1156,
                                    1663,
                                    1158
                                ],
                                "text": "dog!",
                                "confidence": 0.559
                            }
                        ]
                    }
                ]
            }
        ]
    }
}

OCR_SINGLE_WORD = {
	"boundingBox": [
		116,
		654,
		478,
		672,
		477,
		819,
		115,
		818
	],
	"text": "The",
	"confidence": 0.984
}

OCR_SINGLE_WORD_NO_BOUNDING_BOX_KEY = {
	"text": "The",
	"confidence": 0.984
}

OCR_SINGLE_WORD_NO_TEXT_KEY = {
	"boundingBox": [
		116,
		654,
		478,
		672,
		477,
		819,
		115,
		818
	],
	"confidence": 0.984
}

OCR_SINGLE_WORD_NO_CONFIDENCE_KEY = {
	"boundingBox": [
		116,
		654,
		478,
		672,
		477,
		819,
		115,
		818
	],
	"text": "The"
}
# ------------------------------------------------------------------------------------------------
# AZURE OCR PROCESSED RESULTS
# ------------------------------------------------------------------------------------------------
PROCESSED_OCR_RESULTS = [
	{
		"x": 0.3643663194444444, 
		"y": 0.39988425925925924, 
		"width": 0.16905381944444445, 
		"height": 0.09519675925925926, 
		"text": "WORDS", 
		"confidence": 0.981
	}, 
	{
		"x": 0.4598524305555556, 
		"y": 0.5237268518518519, 
		"width": 0.1421440972222222, 
		"height": 0.08796296296296297, 
		"text": "HERE", 
		"confidence": 0.985
	}
]

PROCESSED_OCR_ONE_WORD = [
	{
		"x": 0.3643663194444444, 
		"y": 0.39988425925925924, 
		"width": 0.16905381944444445, 
		"height": 0.09519675925925926, 
		"text": "WORDS", 
		"confidence": 0.981
	}
]

PROCESSED_OCR_NO_CONFIDENCE_KEYS = [
	{
		"x": 0.3643663194444444, 
		"y": 0.39988425925925924, 
		"width": 0.16905381944444445, 
		"height": 0.09519675925925926, 
		"text": "WORDS", 
		"confidence": None
	}, 
	{
		"x": 0.4598524305555556, 
		"y": 0.5237268518518519, 
		"width": 0.1421440972222222, 
		"height": 0.08796296296296297, 
		"text": "HERE", 
		"confidence": None
	}
]

PROCESSED_OCR_ONE_CONFIDENCE_KEY = [
	{
		"x": 0.3643663194444444, 
		"y": 0.39988425925925924, 
		"width": 0.16905381944444445, 
		"height": 0.09519675925925926, 
		"text": "WORDS", 
		"confidence": 0.981
	}, 
	{
		"x": 0.4598524305555556, 
		"y": 0.5237268518518519, 
		"width": 0.1421440972222222, 
		"height": 0.08796296296296297, 
		"text": "HERE", 
		"confidence": None
	}
]

PROCESSED_OCR_TEXT_IN_LINES = [
	{
		'x': 0.013904547162720781, 
		'y': 0.34192530247238295, 
		'width': 0.9526493799323562, 
		'height': 0.10731194108364019, 
		'text': 'The quick brown fox jumps', 
		'confidence': None
	}, 
	{
		'x': 0.06914693724163848, 
		'y': 0.5491846396633351, 
		'width': 0.12251033446072905, 
		'height': 0.04418726985796949, 
		'text': 'over', 
		'confidence': None
	}, 
	{
		'x': 0.2393836903419767, 
		'y': 0.5318253550762756, 
		'width': 0.5031942878617062, 
		'height': 0.0773277222514466, 
		'text': 'the lazy dog!', 
		'confidence': None
	}
]

PROCESSED_OCR_TEXT_SINGLE_WORD = {
	'x': 0.04321683577602405, 
	'y': 0.3440294581799053, 
	'width': 0.13641488162344984, 
	'height': 0.08679642293529721, 
	'text': 'The', 
	'confidence': 0.984
}