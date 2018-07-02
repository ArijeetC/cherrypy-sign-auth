# CherryPy Digital Signature Authentication Tool


#### Files Added

cherrypy/lib/auth_sign.py<br/>
cherrypy/test/test_auth_sign.py<br/>
cherrypy/test/test_private.pem<br/>


#### Files Modified

cherrypy/_cptools.py<br/>
setup.py<br/>
tox.ini<br/>


#### Extra Python Libraries Needed

cryptography==2.2.2


#### How to use this Tool

- First generate RSA private and public key pair
- Private key will be used in client side for signing the message
- Public key will be used in server side to verify the signature
- Add the following lines to your server config dict
        ```'tools.auth_sign.on': True,```<br/>
        ```'tools.auth_sign.realm': host,```<br/>
        ```'tools.auth_sign.key_file': 'keys/public.pem',
        ```
- For client side signature generation, refer to the client.py file

#### Explanation of Client Side Signature Generation (client.py file)

- Private key is loaded from PEM file using cryptography library
- Message is signed using the private key, and signature is generated
- Signature is Base64 encoded and then converted to string
- This string format signature is attached as header to the request

#### Explanation of Signature Verification by the Tool (auth_sign.py file)


- The signature and message header contents are extracted from the request
- In the _verify_signature method, the signature, message and path to the public key PEM file are passed
- The public key is read from the path
- The signature is converted to bytes, then Base64 decoded
- The signature and the message are then verified
- On successful verification, the method returns True, otherwise False
