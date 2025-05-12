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
 source create_env.sh
```

Create the necessary paths and download datasets:
 
```bash
 cd scripts
 source create_paths.sh
 source download_datasets.sh
```

## Execution

### Simplified execution

To reproduce the paper's experiments and reduce the execution time, download the data previously generated. This data contains mobility traces and communication conditions generated with SUMO and the communication model respectively. The total size of all files is up to 200 GB.

### Complete execution

Create SUMOs' trips: 
 
```bash
 cd scripts
 source generate_trips.sh
```

Process the trips:

```bash
 python process_results/processed_mobility.py
```

Generate raw communication:
 
```bash
 cd scripts
 source raw_communication.sh
```

Generate processed communication:

```bash
 source processed_communication.sh
```

Generate delays results:

```bash
 python src/main.py
 python process_results/aggregate_individual_results.py
 python process_results/process_epoch.py
```


## Generate Figures

Training time figure: 

```bash
 python generate_figures/communication.py
```

Epoch time figure: 

```bash
 python generate_figures/epoch.py
```

Accuracy evolution figure: 

```bash
 python generate_figures/time2acc.py
```


Energy figure: 

```bash
 python generate_figures/energy.py
```
