from googletrans import Translator
import json

import os
import json

all_intents = os.listdir(r'C:\Users\21261\Downloads\intents')
translator = Translator()
for intent in all_intents:
    if intent.find('_usersays_en.json') == -1:
        try:
            with open('intents/' + intent) as f:
                data = json.load(f)
            cnt = 0
            for i in data['responses'][0]['messages']:
                if cnt == 0:
                    langue = 'en'
                else:
                    langue = 'en-in'
                i['lang'] = i['lang'].replace(langue, 'fr')
                k = 0
                for j in i['speech']:
                    translated = translator.translate(j, src='en', dest='fr')
                    i['speech'][k] = i['speech'][k].replace(j, translated.text)
                    k += 1
                cnt += 1
        except:
            print(intent)
        with open('new_intents/'+intent, 'w') as f:
            json.dump(data, f)
        try:
            with open('intents/' + intent.replace(".json", "") + '_usersays_en.json') as f:
                data = json.load(f)
            for x in data:
                x['lang'] = x['lang'].replace('en', 'fr')
                for item in x['data']:
                    try:
                        translated = translator.translate(item['text'], src='en', dest='fr')
                        if translated.text == "sommes":
                            translated.text = "es"
                        item['text'] = item['text'].replace(item['text'], translated.text)
                    except:
                        continue
        except:
            print(intent.replace(".json", "") + '_usersays_en.json')
        with open('new_intents/'+intent.replace(".json", "") + '_usersays_en.json', 'w') as f:
            json.dump(data, f)

