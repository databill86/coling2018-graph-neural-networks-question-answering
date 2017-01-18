import pytest
import yaml
import numpy as np
import logging

from questionanswering.datasets import webquestions_io

with open("../questionanswering/default_config.yaml", 'r') as config_file:
    config = yaml.load(config_file.read())

logger = logging.getLogger(__name__)
logger.setLevel(config['logger']['level'])
ch = logging.StreamHandler()
ch.setLevel(config['logger']['level'])
logger.addHandler(ch)

webquestions = webquestions_io.WebQuestions(config['webquestions'], logger=logger)


def test_load_webquestions():
    assert len(webquestions.get_validation_with_gold()) == 2
    assert len(webquestions.get_validation_with_gold()[0]) == 1133


def test_access_sample():
    input_set, targets = webquestions.get_training_samples()
    assert len(input_set) == len(targets)
    if config['webquestions'].get('target.dist'):
        assert len(targets[0]) == config['webquestions'].get('max.negative.samples')
    else:
        assert type(targets[0]) == np.int32
    assert all(['edgeSet' in g for g in input_set[0]])


if __name__ == '__main__':
    pytest.main([__file__])
