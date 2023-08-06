# /usr/bin/env python
import os
from cryptography.fernet import Fernet


def decryptFs(filename,hash, key):
    dataList = []
    for chunkName in hash:
        f = open(str(chunkName), 'rb')
        data = f.read()
        encrypted = Fernet(key).decrypt(data)
        dataList.append(encrypted) 
        f.close()
        os.remove(chunkName)
    f2 = open(("f-"+filename), 'wb')
    for data in dataList:
        f2.write(data)
    f2.close()

    






