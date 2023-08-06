# Python 3 SDK for Baikal

SDK to easilly generate tokens for an application in the 4th platform.

> NOTE: Starting from v0.1.3, the license has changed to Apache 2.0

## Installation

You can install easily with pip:

```bash
pip install baikal-sdk
```

## Usage

**Create a client**
```python
from clients.baikal_client import OpenIDClient


oid_client = OpenIDClient(
    'http://auth.xxx.baikalplatform.com', # authserver endpoint
    'your_oauth_client_id',
    'your_oauth_client_secret',
    # For using grantUser method (jwt-bearer grant type)
    client_keys=[{ 'key': 'stringWithTheKey', format: 'pem' }],  # optional
    issuer='http://yourserver.com/',  # your jwt issuer id
    private_certs_path='/path/to/certs/directory',  # directory to read certificates/private keys.
    verify_certs = False  # Accept self signed certs for authserver communication (not used in token validation)
)
```

**Get an access_token for a user using jwt-bearer**
```python
access_token = oid_client.grant_user(
  'userSUB',
  ['list', 'of', 'scopes'],
  ['list', 'of', 'purposes'],
  authorization_id='46921050-e97c-418b-928c-4158256be92c', # optional
  identifier={'id': 'my-phone-number', 'type': 'phone_number'} # optional
)
```
**Get a client_credentials access_token**
```python
access_token = oid_client.grant_client(
  scopes=['list', 'of', 'scopes'] #optional
  purposes=['list', 'of', 'purposes'] #optional
)
```

**Expose your public keys in a server route to use with a `jwt-bearer`**

If you have configured your issuer in the authserver to read from an endpoint,
you should expose your public keys in an accessible route.

```python
oid_client.get_jwk_set()
```
This will output the public part of your keys to be directly exposed in JWK format (required by authserver and any OIDC server).

## Configuration

The `OpenIDClient` configuration will be read from environment if ommited
```inc
export BAIKAL_AUTHSERVER_ENDPOINT='https://auth.xxx.baikalplatform.com'
export BAIKAL_CLIENT_ID='your_oauth_client_id'
export BAIKAL_CLIENT_SECRET='your_oauth_client_secret'
export BAIKAL_ISSUER='http://yourserver.com/'
export BAIKAL_PRIVATE_CERTS_PATH='/path/to/certs/directory'
```

Supported certs format are (should match the file extension):
* json: JSON stringified JWK
* private: DER encoded 'raw' private key
* pkcs8: DER encoded (unencrypted!) PKCS8 private key
* public: DER encoded SPKI public key (alternate to 'spki')
* spki: DER encoded SPKI public key
* pkix: DER encoded PKIX X.509 certificate
* x509: DER encoded PKIX X.509 certificate
* pem: PEM encoded of PKCS8 / SPKI / PKIX

Grant public methods accept a request config as the last argument,
to allow specifying headers and timeout per-request (in seconds):

```python
access_token = oid_client.grant_client(
    scopes=["scope1"],
    headers={
        'X-Correlator': '1234-5678-9012-3456-7890'
    },
    timeout=30
)
```

## Generate private keys

It's not needed to have private keys generated from a secured authority. For oauth2 verify you can use self-generated keys. Here it's included some tips.

If you want to generate different keys (in JWK format) for development purpose you can use https://mkjwk.org/.

### Generate a RSA private key (with SHA 256 hash, RS256) (using openssl)

````bash
openssl genrsa -des3 -out private-rsa-protected.pem 2048
````

This will produce a private rsa key of 2048 bits protected with a password, in order to remove the password and use directly the private key in the library you can run this:

```bash
openssl rsa -in private-rsa-protected.pem -out private-rsa.pem
# rm private-rsa-protected.pem

```

The private-rsa.pem can be used with the library to generate assertions and to expose the public key part as stated before. Just place the pem in your directory and point the sdk private_certs_path to it.
The public key is automatically generated in JWK as you can check in the expose your public keys section.

It's not recommended to use rsa keys bigger than 2048 (e.g 4096) as the computational cost is not worth. It's better to have a keys rotation policy every given time (e.g. a week). It's also not recommended
to use keys of 1024 length as it can be cracked.
