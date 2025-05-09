# TOFL: Time Optimized Federated Learning


This repository contains the code developed for SBSeg 2025.

## Minimum Requirement

- SO: Ubuntu 20.04.5 LTS or 22.04.5 LTS
- Cores: 24
- Memory: 32 GB


## Installation

Install the requirements:

```bash
 cd scripts
 source create\_env.sh
```

Create the necessary paths and download datasets:
 
```bash
 cd scripts
 source create\_paths.sh
 source download\_datasets.sh
```

## Execution

### Simplified execution

To reproduce the paper's experiments and reduce the execution time, download the data previously generated. This data contains mobility traces and communication conditions generated with SUMO and the communication model respectively. The total size of all files is up to 200 GB.

### Complete execution

Create SUMOs' trips: 
 
```bash
 cd scripts
 source generate\_trips.sh
```

Process the trips:

```bash
 python process\_results/process\_mobility.py
```

Generate raw communication:
 
```bash
 cd scripts
 source raw\_communication.sh
```

Generate processed communication

```bash
 source processed\_communication.sh
```


## Generate Figures


