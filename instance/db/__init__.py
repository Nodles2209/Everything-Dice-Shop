from paths import dbPath
from os import path
from pathlib import Path


def getDBLocation():
    dbLoc = Path(path.join(dbPath, 'app.db'))

    return dbLoc
