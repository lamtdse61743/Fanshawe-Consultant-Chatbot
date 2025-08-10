import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def load_from_json(self, items):
    self.data = items
    self.questions = [item.get('question', '') for item in items]
    self.answers = [item.get('answer', 'No answer provided.') for item in items]