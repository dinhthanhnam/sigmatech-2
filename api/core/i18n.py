import i18n
import os 

def setup_i18n():
    i18n.load_path.append(os.path.join(os.path.dirname(__file__), "..", "lang"))
    i18n.set('locale', 'vi')
    i18n.set('fallback', 'en')