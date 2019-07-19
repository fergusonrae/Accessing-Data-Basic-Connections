###############
### imports ###
###############
from watson_developer_cloud import ToneAnalyzerV3
from constants import CONTENT_TYPE, VERSION, TONE_ANALYZER_URL, LIST_OF_TONES

def create_tone_analyzer(username, password):
    # Create Tone Analyzer Connection
    tone_analyzer = ToneAnalyzerV3(
        username=username,
        password=password,
        version=VERSION,
        url=TONE_ANALYZER_URL
    )
    return tone_analyzer

# Returns all information json datatype
# Will include sentence by sentence tone if available
# Use this if you want to explore everything returned by the call
def get_raw_tone_json(text, tone_analyzer):
    tone = tone_analyzer.tone({"text": text}, CONTENT_TYPE)
    return tone


# Takes text, returns a dictionary of overall document tones and their scores from Watson
# If it fails, returns a dictionary of None objects
# Can fail for many reasons, including just timing out, so error handling should be more robust than this
# Does not return sentence by sentence tones
# TODO: better error handling
def get_clean_tones(text, tone_analyzer):
    dict_of_tones = dict()
    try:
        tone = tone_analyzer.tone({"text": text}, CONTENT_TYPE)
        for tone_results in tone['document_tone']['tones']:
            dict_of_tones[tone_results['tone_name']] = tone_results['score']
        return dict_of_tones
    except:
        for tone in LIST_OF_TONES:
            dict_of_tones[tone] = None
        return dict_of_tones