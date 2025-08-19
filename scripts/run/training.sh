#                            eps tofl  ncl ncf  bs   strategy dataset
source scripts/run/baremetal.sh "3"  "0"  "5" "2" "128" "random" "VeReMi" 
wait

source scripts/run/baremetal.sh "3"  "0"  "5" "2" "128" "random" "WiSec" 
wait

source scripts/run/baremetal.sh "3"  "0"  "5" "2" "128" "m_fastest" "VeReMi" 
wait

source scripts/run/baremetal.sh "3"  "0"  "5" "2" "128" "m_fastest" "WiSec" 
wait
