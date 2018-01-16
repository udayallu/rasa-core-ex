from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings

from rasa_core import __version__ as rasa_core_version
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.channels import HttpInputChannel
from rasa_core.channels.facebook import FacebookInput

logger = logging.getLogger(__name__)

def train_dialogue(domain_file="domain.yml",
                   model_path="models/dialogue",
                   training_data_file="data/stories.md"):

    if rasa_core_version == '0.8.0a4':
        training_data_file="data/stories2.md"

    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy()])

    agent.train(
            training_data_file,
            max_history=3,
            epochs=1000,
            batch_size=50,
            augmentation_factor=50,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent


def train_nlu():
    from rasa_nlu.converters import load_data
    from rasa_nlu.config import RasaNLUConfig
    from rasa_nlu.model import Trainer

    training_data = load_data('data/nlu.json')
    trainer = Trainer(RasaNLUConfig("nlu_config.json"))
    trainer.train(training_data)
    model_directory = trainer.persist('models/nlu/', fixed_model_name="current")

    return model_directory


def run(serve_forever=True):
    interpreter = RasaNLUInterpreter("models/nlu/default/current")
    agent = Agent.load("models/dialogue", interpreter=interpreter)

    input_channel = None
    fb_verify = 'dogs'
    fb_secret = 'ea2738f81a4c837ac6bcf2b446b7898d'
    fb_tokens = None

    if rasa_core_version == '0.8.0a4':
        fb_tokens = 'EAACJuymZCam0BAMLFKDvp864tSzAzczByMcxHtMuqQ8wNR4WKcXjblHKNg9E8EtV2WyJEsYR5WWMDgJ9nbvF4zinJPqQsDNiaMRqs8APvgXIK0ASwKpcWxIpLW5XRD78x1SnypuSirfiVmXBP9qXKTBAZAHaZAdU91qLuDFWQZDZD'
        input_channel = FacebookInput(
            fb_verify,
            fb_secret,
            fb_tokens
        )
    elif rasa_core_version == '0.7.9':
        fb_tokens = {
            '323018891534316': 'EAACJuymZCam0BAMLFKDvp864tSzAzczByMcxHtMuqQ8wNR4WKcXjblHKNg9E8EtV2WyJEsYR5WWMDgJ9nbvF4zinJPqQsDNiaMRqs8APvgXIK0ASwKpcWxIpLW5XRD78x1SnypuSirfiVmXBP9qXKTBAZAHaZAdU91qLuDFWQZDZD',
            '1722277897829614': 'EAACJuymZCam0BALZAZADB1hDap4LDz9zL1URRtjKMQbXwSoFF17hRUxvZBZBcbE6fHAQd1HHmWBZCBYd8rdXR0YYUU3L9WgfQxMXjjpBjLbw8w7ZCMcHFL5X9xZB7NkZBXWDZAZBNH8WMf6mlgYDTu9EJd4SmLdm4qefqZADos0gPHY1RwZDZD',
        }
        input_channel = FacebookInput(
            fb_verify,
            fb_secret,
            fb_tokens,
            True
        )
    


    if serve_forever:
        agent.handle_channel(HttpInputChannel(5000, '/app', input_channel))
    return agent


if __name__ == '__main__':
    if rasa_core_version == '0.8.0a4':
        utils.configure_colored_logging(loglevel="DEBUG")
    try:
        parser = argparse.ArgumentParser(description='starts the bot')

        parser.add_argument(
                'task',
                choices=["train-nlu", "train-dialogue", "run"],
                help="what the bot should do - e.g. run or train?")
        task = parser.parse_args().task

        # decide what to do based on first parameter of the script
        if task == "train-nlu":
            train_nlu()
        elif task == "train-dialogue":
            train_dialogue()
        elif task == "run":
            run()
        else:
            warnings.warn("Need to pass either 'train-nlu', 'train-dialogue' or "
                        "'run' to use the script.")
            exit(1)
    except KeyboardInterrupt:
        exit(1)
