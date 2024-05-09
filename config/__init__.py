from paths import dbPath


def getSQLPath():
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{dbPath}/app.db"
    return SQLALCHEMY_DATABASE_URI
