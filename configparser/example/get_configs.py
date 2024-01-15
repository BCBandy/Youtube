import configparser


config = configparser.ConfigParser()
config.read(r'C:\Users\b_ban\Documents\VSCode\Youtube\configparser\example\config.ini')

api_secret = config['api.keys']['API_SECRET']
api_key = config['api.keys']['API_KEY']

print(api_key)
print(api_secret)

config['app.setting'] = {}
config['app.setting']['value1'] = 'settings1_5483257409'
config['app.setting']['value2'] = 'settings2_74099999'

config['dict.setting'] = {
    'val1': 5432,
    'val2': 54325
}

print(config['app.setting']['running'])

with open(r'C:\Users\b_ban\Documents\VSCode\Youtube\configparser\example\config.ini', 'w') as file:
    config.write(file)


