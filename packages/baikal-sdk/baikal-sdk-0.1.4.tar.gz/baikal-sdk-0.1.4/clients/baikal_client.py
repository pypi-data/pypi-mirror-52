"""Http clients to get tokens from 4P authserver using OIDC protocol"""
__author__ = 'eag'
__license__ = "see LICENSE file"

import json
import logging
import random
from collections import namedtuple
from datetime import timedelta, datetime
from pathlib import Path

import requests
from jose import jwt, jws, JWSError
from jose.backends import RSAKey, ECKey
from jose.constants import ALGORITHMS
from requests.auth import HTTPBasicAuth

from clients.cache import lru_cache
from clients.exceptions import ConfigurationError, AuthserverError, InvalidSignature

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
AuthserverConfig = namedtuple('AuthserverConfig', ['issuer', 'token_endpoint', 'jwks'])
ASSERTION_EXP_GAP = timedelta(minutes=60)
DEFAULT_REQUEST_TIMEOUT = 10  # timeout in seconds to wait for a response from authserver
TTL_CACHE = 1
NTTL_CACHE = 30 * 60
SIZE_CACHE = 10


@lru_cache(max_size=SIZE_CACHE, ttl=TTL_CACHE, nttl=NTTL_CACHE)
def get_authserver_config(authserver_endpoint, verify_certs=True):
    """
    It returns the configuration needed in our client of the authserver 4P:
        token endpoint and public keys in jwk format
    :param verify_certs:
    :param authserver_endpoint:
    :return: namedtupl
    """
    if authserver_endpoint.endswith('/'):
        authserver_endpoint = authserver_endpoint[:-1]

    well_known_uri = authserver_endpoint + "/.well-known/openid-configuration"
    r = requests.get(well_known_uri, verify=verify_certs)
    config = r.json()
    token_endpoint = config['token_endpoint']
    issuer = config['issuer']
    jwks_uri = config['jwks_uri']
    r = requests.get(jwks_uri, verify=verify_certs)
    jwks = r.json()
    return AuthserverConfig(issuer=issuer, token_endpoint=token_endpoint, jwks=jwks)


def guess_key(key_path):
    """
    Guess the key format of the key in path given and return the  key
    :param key_path:
    :return:
    """

    # Try RSA keys (most common with hassh SHA256 -> RS256 alg)
    try:
        key_content = Path(key_path).read_text()
        key = RSAKey(key_content, ALGORITHMS.RS256)
        key.to_dict()
        return key
    except Exception as e:
        logger.debug("RSA key %s invalid: %s", key_path, str(e))

    # Try EC keys (most common with hassh SHA256 -> ES256 alg)
    try:
        key_content = Path(key_path).read_text()
        key = ECKey(key_content, ALGORITHMS.ES256)
        key.to_dict()
        return key
    except Exception as e:
        logger.debug("EC key %s invalid: %s", key_path, str(e))

    return None


def load_jwk_set(path, keys):
    """
    It builds  JWKS set, (private and public) with the private keys found that will be used for signing assertions in jwt-bearer and expose the set in public format
    :param path: path to all private keys files
    :param keys: list of keys in string format
    :return: a tuple with private and public keys in dict format following JWK format
    """
    keys_private = []
    keys_public = []
    if path:
        for filename in Path(path).iterdir():
            key = guess_key(filename)
            if not key:
                logger.warning("The key %s is not supported", filename)
            else:
                keys_private.append(key.to_dict())
                keys_public.append(key.public_key().to_dict())

    return {'keys': keys_private}, {'keys': keys_public}


def ensure_string(in_bytes):
    try:
        return in_bytes.decode('UTF-8')
    except Exception:
        return in_bytes


class OpenIDClient(object):

    def __init__(self, authserver_endpoint, client_id, client_secret, client_keys=None, issuer=None,
                 private_certs_path=None, verify_certs=True):
        self.verify_certs = verify_certs
        if not self.verify_certs:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._authserver_endpoint = authserver_endpoint
        self._authserver_auth = HTTPBasicAuth(client_id, client_secret)
        self.issuer = issuer
        self.private_keys, self.public_keys = load_jwk_set(private_certs_path, client_keys)

    @property
    def authserver_config(self):
        return get_authserver_config(self._authserver_endpoint, verify_certs=self.verify_certs)

    def get_random_key(self):
        return random.choice(self.private_keys['keys'])

    def grant_user(self, sub, scopes, purposes, authorization_id=None, identifier=None, headers={},
                   timeout=DEFAULT_REQUEST_TIMEOUT):
        if not self.issuer:
            raise ConfigurationError("Issuer should be defined to generate tokens with jwt-bearer")
        if not self.private_keys:
            raise ConfigurationError("No private keys found for generating assertion")

        now = datetime.utcnow()  # jose library converts to epoch time
        payload = {
            'sub': sub,
            'active': True,
            'scope': ' '.join(scopes),
            'purpose': ' '.join(purposes),
            'exp': now + ASSERTION_EXP_GAP,
            'iat': now,
            'iss': self.issuer,
            'aud': self.authserver_config.issuer
        }
        if authorization_id:
            payload['authorization_id'] = authorization_id

        if identifier:
            payload['identifier'] = identifier
        key = self.get_random_key()
        assertion = jwt.encode(payload, key, algorithm=key['alg'])
        body = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': assertion
        }

        return self._call_token_endpoint(body, headers, timeout)

    def grant_client(self, scopes=None, purposes=None, headers={}, timeout=DEFAULT_REQUEST_TIMEOUT):
        body = {
            'grant_type': 'client_credentials'
        }
        if scopes:
            body['scope'] = ' '.join(scopes)
        if purposes:
            body['purposes'] = ' '.join(purposes)
        return self._call_token_endpoint(body, headers, timeout)

    @staticmethod
    def _parse_error(response):
        try:
            error = response.json()
            return str(error)
        except ValueError:
            return "Unexpected response from authserver: status_code " + response.status_code + "; resp: " + response.text

    def _call_token_endpoint(self, body, headers, timeout):
        r = requests.post(self.authserver_config.token_endpoint, body, auth=self._authserver_auth,
                          verify=self.verify_certs, headers=headers, timeout=timeout)
        if r.status_code == requests.codes.unauthorized:
            raise AuthserverError("The credentials client_id/client_secret are invalid.")
        elif r.status_code != requests.codes.ok:
            raise AuthserverError("Error from token endpoint of Authserver: " + self._parse_error(r))

        access_token = r.json()['access_token']
        self._verify_signature(access_token)
        return access_token

    def _verify_signature(self, access_token):
        try:
            header = jws.get_unverified_header(access_token)
            jws.verify(access_token, self.authserver_config.jwks, header['alg'])
        except JWSError as e:
            raise InvalidSignature("Error verifying signature of access_token: " + str(e))

    def get_jwk_set(self):
        public_key_jwk_serialized = map(lambda key: {k: ensure_string(v) for k, v in key.items()},
                                        self.public_keys['keys'])
        return json.dumps({'keys': list(public_key_jwk_serialized)})
