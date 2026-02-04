from phola_park_app.model import Survey

SURVEY_MAP = {
    "survey1": ["Water", "Electricity"],
    "survey2": ["Health", "Crime"],
    "survey3": ["Community", "Infrastructure"],
}

def get_surveys_for_page(page_key):
    topics = SURVEY_MAP.get(page_key, [])
    return Survey.query.filter(Survey.topic.in_(topics)).all()
