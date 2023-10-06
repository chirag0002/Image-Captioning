from datetime import datetime, timedelta
import requests
from jwt import encode
import base64

api_key = 'f19b06f345005353ae7278ce64e896eb'
account_key_id = '465'

payload = {
	'account_key_id': account_key_id,
	'exp': datetime.utcnow() + timedelta(days=1),
	'iat': datetime.utcnow()
}

jwt_token = encode(payload, key=api_key, algorithm='HS256')

image_file_path = 'Images/six.jpeg'

with open(image_file_path, 'rb') as image_file:
    base64_img_str = base64.b64encode(image_file.read()).decode('utf-8')

r = requests.post('https://api.phosus.com/icaption/v1',headers={'authorizationToken': jwt_token}, json={'image_b64': base64_img_str})
r.raise_for_status()  
prediction = r.json()["prediction"]
print(prediction)
