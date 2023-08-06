import ipfshttpclient
import json
from json.decoder import JSONDecodeError
from medblocks import cryptography
from medblocks.errors import *
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

IPFS_PORT = "5001"
MEDBLOCKS_PORT = "8080"

    
class Client(object):
    def __init__(self, ip_address, *args, **kwargs):
        self.reference_mapping = {}
        self.base_url = "http://{ip_address}:{port}/".format(ip_address=ip_address, port=MEDBLOCKS_PORT)
        self.ipfs = ipfshttpclient.connect("/ip4/{ip_address}/tcp/{port}/http/".format(ip_address=ip_address, port=IPFS_PORT))
        self.logged_in = False
        
    def _check_login(self):
        if self.logged_in:
            return
        else:
            raise LoginError("Please login and then try again")

    def medblocks(self, endpoint, json={}):
        url = self.base_url + "{}".format(endpoint)
        r = requests.post(url, json=json)
        try:
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError: # TODO Check backend for JSON in errors
            raise MedBlocksAPIError(r.text)

    def _checkReferences(dict):
        """Checks dictionary for references and replaces them with known references or throws error"""

    def list(self, **kwargs):
        """
        Optional kwargs:
        ownerEmailId (string): Lists all medblocks that belong to the owner
        permittedEmailId (string): List all medblocks that this email has permission to
        """
        return self.medblocks("list", kwargs)
    
    def register(self, emailId, password):
        """
        Generates a key pair, encrypts with as password and stores it on the server. Registers a 
        """
        keypairs = cryptography.generateKeys(password)
        keypairs["emailId"] = emailId
        self.medblocks("storeKey", keypairs)
        return self.medblocks("register",{
            "emailId": emailId,
            "sPublicKey": keypairs["sPublicKey"],
            "ePublicKey": keypairs["ePublicKey"]
            })
    
    def login(self, emailId, password, offlineKeys=None):
        if offlineKeys is None:
            keys = self.medblocks("getKey", {"emailId": emailId})
        else:
            keys = offlineKeys
        self.ePrivateKey = cryptography.decryptKey(keys["ePrivateKey"].encode(), keys["IV"]["IVE"].encode(), password)
        self.sPrivateKey = cryptography.decryptKey(keys["sPrivateKey"].encode(), keys["IV"]["IVS"].encode(), password)
        self.ePublicKey = cryptography.get_publicKey(self.ePrivateKey)
        self.sPublicKey = cryptography.get_publicKey(self.sPrivateKey)
        self.emailId = emailId
        self.logged_in = True
        return
    
    def getPublicKey(self, email):
        user = self.medblocks("getUser", {"emailId": email})
        return user["ePublicKey"]

    def prepare_payload(self, dict):
        data = json.dumps(dict)
        signature = cryptography.generate_signature(data, self.sPrivateKey)
        payload = {"data":data, "signature": signature.decode()}
        return payload

    def addBlock(self, bytes, to_address, name, open=False):
        self._check_login()

        if open:
            r = self.ipfs.add_bytes(bytes)
            data = {
            "ipfsHash": r,
            "IV": "NO ENCRYPTION",
            "name": name,
            "format": "fhir/json",
            "creatorEmailId": self.emailId,
            "ownerEmailId": self.emailId,
            "permissions":[
            ]
        }
        else:
            encryption_start = time.time()
            public_key = self.getPublicKey(to_address)
            aes_key = cryptography.generate_aes_key()
            encrypted_file, iv = cryptography.encrypt_file(bytes, aes_key)
            access_key = cryptography.create_access_key(aes_key, public_key)   
            encryption_elapsed = round(time.time() - encryption_start, 2)
            ipfs_start = time.time()
            r = self.ipfs.add_bytes(encrypted_file)
            ipfs_elapsed = round(time.time() - ipfs_start, 2)
            iv = iv.decode()
            data = {
                "ipfsHash": r,
                "IV": iv,
                "name": name,
                "format": "fhir/json",
                "creatorEmailId": self.emailId,
                "ownerEmailId": self.emailId,
                "permissions":[
                {"receiverEmailId": to_address, 
                "receiverKey":access_key.decode()}
                ]
            }
        
        signing_start = time.time()
        payload = self.prepare_payload(data)
        signing_elapsed = round(time.time() - signing_start)
        request_start = time.time()
        medblock = self.medblocks("addBlock", payload)
        request_elapsed = round(time.time() - request_start, 2)
        # print("Time elapsed: encryption: {}sec | ipfs: {}sec | signing: {}sec | request: {}".format(encryption_elapsed, ipfs_elapsed, signing_elapsed, request_elapsed))
        return medblock
    
    def extractKey(self, block):
        self._check_login()
        permissions = block["permissions"]
        for p in permissions:
            if p["receiverEmailId"] == self.emailId:
                accessKey = p["receiverKey"]
        try:
            aes_key = cryptography.decrypt_access_key(accessKey, self.ePrivateKey)
            return aes_key
        except NameError:
            raise PermissionError("No access key for current user found. To view raw block set raw=True")

    def getBlock(self, ipfsHash, raw=False):
        block = self.medblocks("getBlock",{"ipfsHash":ipfsHash})
        if raw:
            return block
        aes_key = self.extractKey(block)
        iv = block["IV"].encode()
        encrypted = self.ipfs.cat(ipfsHash)
        decrypted = cryptography.decrypt_file(encrypted, aes_key, iv)
        return decrypted

    def addPermission(self, ipfsHash, to):
        self._check_login()
        public_key = self.getPublicKey(to)
        block = self.medblocks("getBlock",{"ipfsHash":ipfsHash})
        aes_key = self.extractKey(block)
        accessKey = cryptography.create_access_key(aes_key, public_key)
        data = {
            "ipfsHash": ipfsHash,
            "senderEmailId": self.emailId,
            "permissions": [
                {
                    "receiverEmailId": to,
                    "receiverKey": accessKey.decode()
                }
            ]
        }
        payload = self.prepare_payload(data)
        return self.medblocks("addPermission", payload)

    def logout(self):
        self.ePublicKey = None
        self.sPublicKey = None
        self.ePrivateKey = None
        self.sPrivateKey = None
        self.logged_in = False
        return

    def async_add_medblock(self, uuid, data):
        start_time = time.time()
        medblock = self.addBlock(data, self.emailId, "ORIGIN")
        hash = medblock["ipfsHash"]
        elapsed = round(time.time() - start_time, 2)
        self.reference_mapping[uuid] = hash
        print("addBlock completed {} -> {} ({} secs)".format(uuid, hash, elapsed))
    
    def addFhir(self, data, version="R4", max_workers=10):
        start = time.time()
        for resource in data["entry"]:
            fullUrl = resource.pop("fullUrl")
            resource["resource"].pop("id")
            self.reference_mapping[fullUrl] = resource
        # with ThreadPoolExecutor(3) as f:
        #     for i in range(100):
        #         f.submit(self.test_async, i, i)
        
        with ThreadPoolExecutor(max_workers) as f:
            for uuid in self.reference_mapping.keys():
                data = self.reference_mapping[uuid]
                data = json.dumps(data).encode()
                # self.async_add_medblock(uuid, data)
                f.submit(self.async_add_medblock, uuid, data)
        elapsed = round(time.time() - start, 2)
        print("Finished addBlock for {} in {} secs".format(len(self.reference_mapping.keys()), elapsed))
        mapping = self.reference_mapping
        self.addBlock(json.dumps(mapping).encode(), self.emailId, "MAP", open=True)
        self.reference_mapping = {}
        return mapping