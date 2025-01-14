#!/bin/bash

# Author: Jose Carlos
# Contact Telegram: @josectheone
# Credits to "AG" for sharing the base script

# Set static variables
# Set home folder as default install path (cd ~)
wallet=$(cd ~; LD_LIBRARY_PATH=. ./wallet.sh -t list | grep account | awk '{print $2}');
# Defines the shard to use
shardid=$(grep -Eom1 "\"shardID\"\:[0-9]+" latest/validator*.log | awk -F: '{print $2}');
# Defines the base ammount to send in every TX
amount=0.001$(($RANDOM + 1));

while true; do
# Set dinamic variables 
pga_out=$(curl -s https://harmony.one/pga/network.json);
nodes_online_count=$(echo "${pga_out}" |  jq '.shards."'$shardid'".node_count.online');
rand=$(( $(($RANDOM % $nodes_online_count)) - 1 ));
recipient=$(echo "${pga_out}" | jq -r '.shards."'$shardid'".nodes.online | map(select(. != "'$wallet'")) | .['$rand']');

# Run wallet transfers
./wallet.sh -t transfer --from $wallet --to $recipient --amount $amount --shardID $shardid --toShardID 0 --pass pass: & wait & sleep 10
done
