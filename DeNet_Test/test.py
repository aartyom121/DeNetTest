import requests

# Получение баланса для одного адреса
response = requests.get('http://127.0.0.1:8000/get_balance/', params={'address': '0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d'})
print(response.json())

# Получение балансов для нескольких адресов
response = requests.post('http://127.0.0.1:8000/get_balance_batch/', data={'addresses[]': ['0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d', '0x4830AF4aB9cd9E381602aE50f71AE481a7727f7C']})
print(response.json())
