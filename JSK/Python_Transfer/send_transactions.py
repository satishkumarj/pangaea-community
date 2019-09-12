import requests
import os
import sys
import getopt
import time
import pandas as pd
import io

argv = sys.argv[1:]
wallet = ''
shardId = ''
sent_addresses_file = "sent_addresses.txt" 
try:
    opts, args = getopt.getopt(argv,"a:s:",["walletaddress=", "sharedid="])
except getopt.GetoptError:
    print('python3 send_transactions.py -a your_wallet_address -s shard_id')
    sys.exit(2)
for opt, arg in opts:
   if opt in ("-a", "--walletaddress"):
       wallet = arg
   elif opt in ("-s", "--sharedid"):
       shardId = arg
if wallet == '' or shardId == '':
   print('python3 send_transactions.py -a your_wallet_address -s shard_id')
   sys.exit(2)

while(1):    
    url = "https://harmony.one/pga/network.csv"
    s = requests.get(url).content
    ds = pd.read_csv(io.StringIO(s.decode('utf-8')))

    if os.path.exists(sent_addresses_file):
        with open(sent_addresses_file, 'r') as f:
            sent_addresses = f.read().replace('\n', ' ')
    else:
        sent_addresses = []
    
    for  index,row in ds.iterrows():
        addr = row["Address"]
        to_shardId = row["Shard"]
        if sent_addresses.find(addr) < 0:
            if row["Online"]:
                transfer = './wallet.sh -t transfer --from {} --to {} --amount 0.01 --pass pass:  --toShardID {} --shardID {}'.format(wallet, addr, to_shardId, shardId)
                try:
                    print("Sending 0.01 ONE to {}".format(addr))
                    os.system(transfer)    
                except getopt.GetoptError:
                    print('Exiting due to error executing transfer')
                    sys.exit(2)
                #if i == 1:
                #    sys.exit(2)
                with open(sent_addresses_file, 'a+') as f:
                    f.write("%s " % addr)
                time.sleep(2)
    
    open(sent_addresses_file, "w").close()
