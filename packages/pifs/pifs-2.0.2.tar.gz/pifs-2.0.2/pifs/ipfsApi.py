# /usr/bin/env python
import ipfshttpclient

def ipfsFileAdd(filename):
    api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http') 
    ipfsLoadedFile = api.add(filename)
    ipfsHash = (ipfsLoadedFile['Hash'])
    return ipfsHash

def ipfsFileget(hash):
    api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    api.get(hash)