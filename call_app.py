import requests
response = requests.get('http://localhost:5000/call-api')
if response.status_code == 200:
    print('Data:', response.json())
else:
    print('Failed to retrieve data:', response.status_code)