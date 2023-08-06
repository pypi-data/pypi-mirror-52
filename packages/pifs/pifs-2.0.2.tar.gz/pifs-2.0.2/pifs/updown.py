# /usr/bin/env python
import sys, os, argparse
from .encrypt import encryptFs
from .decrypt import decryptFs
from .ipfsApi import ipfsFileget,ipfsFileAdd
import inspect


parser = argparse.ArgumentParser(add_help=False, description='pifs mini command line tools')
parser.add_argument("-ef", "--encyptfile", default="Empty", type = str, dest="ecfile", help=argparse.SUPPRESS)
parser.add_argument("-df", "--decyptfile", default="Empty", type = str, dest="defile", help=argparse.SUPPRESS)

parser.add_argument('-h', '--help', action='store_true')
args = parser.parse_args()
       

def ipfsUpload(filename):
    try:
        hash = []
        encryptFs(filename)
        for i in range(1,31):
            fn1 = filename + "-%s" % (i)
            ipfsFileAdd(fn1)
            h = ipfsFileAdd(fn1)
            hash.append(h)
            os.remove(fn1)
        with open(os.path.join("./KeyHash/",(filename + '-hash.txt')), 'w') as f:
            for item in hash:
                f.write("%s\n" % item)
        print("Upload successes")
    except:
        for i in range(1,31):
            fn1 = filename + "-%s" % (i)
            os.remove(fn1)
        print("Fail to Upload")
        print("make sure you have run > ipfs daemon")

def ipfsDownload(filename):
    try:  
        fn1 = filename + "-hash.txt"
        key1 = "key-" + filename + ".pem"
        hash = [line.rstrip('\n') for line in open(os.path.join('./KeyHash/',fn1))]
        f = open(os.path.join('./KeyHash/',key1))
        key = f.read()
        for i in hash:
            ipfsFileget(i)
        decryptFs(filename,hash, key)
        print("Download successes")
    except:
        print("Download fail")
        print("make sure you have run > ipfs daemon")

ecfile = args.ecfile
defile = args.defile

if args.help:
    print("""
        pifs mini command line tools

        -h or --help bring help message to about pifs 
    
        -e, --encrypt   upload and encrypting files
        -f, --file      specified file name e.g: pi-movie.mov
        -d, --decrypt   specified key to decrypt and restrive file with filename called

        usage

        pifs -ef filename (e.g: filename = movie.mov) upload movie.mov to p2p nodes
        pifs -df filename (e.g: filename = movie.mov) download movie.mov from p2p 
          """)
def run():
    if(ecfile!="Empty"):
        ipfsUpload(ecfile)
    elif(defile!="Empty"):
        ipfsDownload(defile)