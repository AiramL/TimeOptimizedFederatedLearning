# This code executes the federated learning training, starting clients and server
#                                            eps  tofl  ncl ncf  bs   strategy dataset
source scripts/run/all_clients_baremetal.sh "40"  "0"  "100" "16" "128" "random" "VeReMi" & 
source scripts/run/all_clients_baremetal.sh "40"  "0"  "100" "16" "128" "random" "WiSec" & 
source scripts/run/all_clients_baremetal.sh "40"  "0"  "100" "16" "128" "m_fastest" "VeReMi" & 
source scripts/run/all_clients_baremetal.sh "40"  "0"  "100" "16" "128" "m_fastest" "WiSec" & 
source scripts/run/all_clients_baremetal.sh "40"  "0"  "100" "95" "128" "random" "VeReMi" & 
source scripts/run/all_clients_baremetal.sh "40"  "0"  "100" "95" "128" "random" "WiSec" & 
source scripts/run/all_clients_baremetal.sh "40"  "0"  "100" "95" "128" "m_fastest" "VeReMi" & 
source scripts/run/all_clients_baremetal.sh "40"  "0"  "100" "95" "128" "m_fastest" "WiSec" & 
