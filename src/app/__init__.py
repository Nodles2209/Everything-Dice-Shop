import os
from paths import configPath
from config import getSQLPath


def getConfig():
    config = os.path.join(configPath, 'config.cfg')

    return config

