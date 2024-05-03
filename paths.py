import os

rootPath = os.path.dirname(os.path.abspath(__file__))
configPath = os.path.join(rootPath, 'config')
instancePath = os.path.join(rootPath, 'instance')
dbPath = os.path.join(instancePath, 'db')
jsonPath = os.path.join(instancePath, 'json')
srcPath = os.path.join(rootPath, 'src')
appPath = os.path.join(srcPath, 'app')
