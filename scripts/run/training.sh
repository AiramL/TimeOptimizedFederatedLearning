# This code executes the federated learning training, starting clients and server
#                            eps tofl  ncl ncf  bs   strategy dataset
source scripts/run/baremetal.sh "40"  "0"  "20" "4" "128" "random" "VeReMi" & 
wait

source scripts/run/baremetal.sh "40"  "0"  "20" "4" "128" "random" "WiSec" &
wait

source scripts/run/baremetal.sh "40"  "0"  "20" "4" "128" "m_fastest" "VeReMi" & 
wait

source scripts/run/baremetal.sh "40"  "0"  "20" "4" "128" "m_fastest" "WiSec" &
wait
