# This code executes the federated learning training, starting clients and server
#                                eps  tofl   ncl ncf  bs   strategy dataset
#source scripts/run/baremetal.sh "40"  "0"  "20" "2" "128" "random" "VeReMi" & 
#wait

#source scripts/run/baremetal.sh  "40"  "0"  "20" "2" "128" "random" "WiSec" &
#wait
#

source scripts/run/baremetal.sh "40"  "0"   "20" "16" "126" "random" "VeReMi" & 
wait

source scripts/run/baremetal.sh  "40"  "0"  "20" "16" "126" "random" "WiSec" &
wait

source scripts/run/baremetal.sh  "40"  "0"  "20" "2" "128" "m_fastest" "VeReMi" & 
wait

source scripts/run/baremetal.sh  "40"  "0"  "20" "2" "128" "m_fastest" "WiSec" &
wait 

source scripts/run/baremetal.sh  "40"  "0"  "20" "16" "126" "m_fastest" "VeReMi" & 
wait

source scripts/run/baremetal.sh  "40"  "0"  "20" "16" "126" "m_fastest" "WiSec" &
wait
