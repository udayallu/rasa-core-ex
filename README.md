# Rasa Core Example

Integrated with Facebook Messenger

Python 2.7

Install packages:
```
pip install rasa_core rasa_nlu spacy flask scikit-learn sklearn-crfsuite
python -m spacy download en
```

Train NLU model:
```
python -m rasa_nlu.train -c nlu_config.json --fixed_model_name default/current
```

Train Dialogue:
```
python -m rasa_core.train -s data/stories2.md -d domain.yml -o models/dialogue --epochs 1000
```

Run server:
```
python bot.py run
```
