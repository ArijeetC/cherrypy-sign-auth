#Client Python code

import requests
import time
import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def generate_signature(time_millis):

    message = time_millis.encode('utf-8')

    with open('keys/private.pem', 'rb') as file:
        private_key = serialization.load_pem_private_key(
            file.read(),
            password=None,
            backend=default_backend()
        )

    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )


    # signature is base64 encode, then converted to string
    signature = base64.b64encode(signature).decode()

    return signature



def send_request(url="http://localhost:8081/app", method="GET"):

    time_millis = str(int(round(time.time() * 1000)))

    signature = generate_signature(time_millis)

    signature = signature

    headers = {'signature': signature, 'message': time_millis}

    if method == "GET":
        resp = requests.get(url, headers=headers)
    else:
        resp = requests.post(url, headers=headers)

    return resp


def main(url):

    resp = send_request(url=url)
    print(resp.content.decode())


if __name__=='__main__':
   import sys
   url = sys.argv[1]
   main(url)
