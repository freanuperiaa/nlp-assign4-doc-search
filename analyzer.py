import json
import spacy
import re



def update_tokens_json(new_data):
    with open('tokens.json') as f:
        data = json.load(f)
    data.update(new_data)
    with open('tokens.json', 'w') as f:
        json.dump(data, f)


def add_to_token(text_from_pdf, filename):
    nlp = spacy.load("en_core_web_sm")
    cleaned_text = re.sub(r'(\s+\d\s+)|([\r\n]+)|(\s+)', ' ', text_from_pdf)
    doc = nlp(cleaned_text)
    entities = []
    for ent in doc.ents:
        entities.append(str(ent))
    data = {filename: {
        "entities": entities
    }}
    update_tokens_json(data)


def search_files(search_requests):
    regex = ""
    for search_request in search_requests:
        regex += f"({search_request.lower()})|"

    if len(regex) > 0:
        regex = regex[0:-1]

    with open('tokens.json') as f:
        data = json.load(f)
    files = []
    id_ = 1
    for article in data:
        for key, entities in data[article].items():
            for entity in entities:
                if re.match(rf"{regex}", entity.lower()):
                    files.append([id_, re.sub("_", " ", article.split('.')[0]), article])
                    id_ += 1
                    break
    return files