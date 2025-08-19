# TOFL: Time Optimized Federated Learning

Vehicular networks face cyber threats that can harm drivers, passengers, and pedestrians. In this scenario, federated learning is a possible solution to train models that detect threats without violating user privacy. However, federated learning is particularly sensitive to communication delays, which is a natural consequence of high mobility in vehicular networks. This problem is commonly ignored in the literature, which does not consider the possibility of network disconnections. This work proposes a client selection strategy designed to minimize the training time of a machine learning model for vehicular threat detection, considering the communication time that varies according to the movement of clients. The results demonstrate that TOFL, using only 20% of the total available clients, can reduce the time required to achieve high accuracy by up to 50% compared to state-of-the-art approaches, while reducing the resource consumption of client devices.

This repository contains the code developed for SBSeg 2025. The code is composed by three parts. The first part simulates vehicles mobility, to extract this pattern to estimate the user delays, on the second part, using 5G technology. Finally, the third part simulates the federated learning training, given the latency values obtained during the first and second parts. The object is to test different client selection strategies in a scenario with mobility.

# Security considerations

Our code only uses CSV files pre-processed from simulated CAM data. Therefore, this code does not impose any risk for the host during its execution.

# Considered Stamps

We aim to obtain all four stamps from the conference: available, functional, sustainable, and reproducible.


# Minimum Requirement

- SO: Ubuntu 22.04.5 LTS
- Cores: 2
- Memory: 2 GB
- Storage: 40 GB

## Estimated execution time

The time must vary due to your networking conditions to get the necessary packages. Additionally, the entire execution time depends on the hyperparameters chosen for the test. Therefore, we select 5 cars and 3 epochs for the minimum test, which should take around 30 minutes to build from scratch the whole environment.

# Dependencies 

## This repository has the following dependencies: 

- VirtualBox 7.1.12 (for the VM execution only)
- Git command 2.34.1
- Python3.12
- Conda 25.5.1
- SUMO 1.24.0
- pandas 2.3.1
- numpy 1.26.4
- torch 2.3.0
- torchvision 0.18.0
- matplotlib 3.10.3
- flower 1.7.0
- tensorflow 2.19.0
- scikit-learn 1.7.1
- seaborn 0.13.2
- scikit-image 0.25.2

# Virtual Machine Installation

The entire environment was virtualized to facilitate easier execution. You can download the virtual machine image from the following address:
```bash
https://gta.ufrj.br/~airam/tofl.ova
```
Load the image on VirtualBox to execute the experiments and execute all commands with root user.
```bash
user: root
password: SBS3g2025
```
When using the provided virtual machine, you can skip directly to the section [Execution](#execution).

# Baremetal Installation (30 minutes)

If you want to install from scratch, the dependencies must be installed. Firstly, we install conda to manage the virtual environment. Then, we install TOFL by cloning the git repository.

## Conda (2 minutes)

### Get the script to install miniconda
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

### Change script permissions
```bash
chmod +x Miniconda3-latest-Linux-x86_64.sh
```

### Execute installation
```bash
./Miniconda3-latest-Linux-x86_64.sh
```
Accept all the conditions and choose the path to install miniconda3, by default, it is located on /root/miniconda3.

### Run environment
```bash
source ~/.bashrc
```

## TOFL (28 minutes)

### Clone this repository:
```bash
git clone https://github.com/AiramL/TimeOptimizedFederatedLearning.git
```
### Change to the new directory
```bash
cd TimeOptimizedFederatedLearning
```

### Create paths
```bash
source scripts/build/paths.sh
```

### Accept the terms
During the installation of dependencies and environment, you might be asked to accept the terms of conda and SUMO. Make sure to enter yes. Also, the conda environment must be activated after its installation.

### Install dependencies (5 minutes)
```bash
source scripts/build/dependencies.sh
```

### Create the virtual environment (18 minutes)
```bash
source scripts/build/env.sh
```

### Download datasets (5 minutes)
```bash
source scripts/build/datasets.sh
```

# Execution (< 10 minutes)

All the codes were executed with the root user on a virtual machine. If you are using your machine without virtualization, you can execute the commands with your local user.

## Minimum test

We consider that the minimum test is to reproduce the figures in the paper. Therefore, we provide a simplified execution, which uses different parameters from the paper. The reduced parameters are listed below:

- Number of clients: 5
- Number of epochs: 3
- SUMO simulation time: 600 seconds
- Client's speed: 50 km/h
- Scenario: Manhattan
- Grid size: 600 x 600 
- Car model: Krauss
- Number of executions: 10

### Create SUMOs' trips (2 minutes): 

Firstly, we need to create the mobility pattern of federated learning clients. We do this by executing sumo in a Manhattan grid.
 
```bash
source scripts/run/raw/mobility.sh
```
Expected output: 
```bash
PHASE 1 -> Generating the grid topology
Success.
....... -> Copy netfile to the current directory 
....... -> Generate continuous rerouters 
....... -> Generating random flows for JTRROUTER 
....... -> Run SUMO for configuration Krauss 5 cars / iteration 0
....... -> Generate tr file for configuration 5 cars / iteration 0
One or more coordinates are negative, some applications might need strictly positive values. To avoid this use the option --shift
```

### Process trips (< 1 second):

SUMO generates raw files about users' mobility, which we need to extract to use as input for the communication model.

```bash
source scripts/run/processed/mobility.sh
```
Expected output: 
```bash
process finished
```

### Channel Model

The communication model takes the processed SUMO output to determine the clients' delays. It generates 30 raw simulations that we use to compute the average user throughput. For the communication model we use the 3GPP TR 38.901, the most versatile and widely accepted channel model. It can handle urban, rural, and highway scenarios with realistic parameters for Doppler shift, path loss, and multi-path propagation. For detailed intersection scenarios, consider using TAPAS V2X or Geometry-Based Stochastic Models.

Overview:
- Standardized by 3GPP for 5G.
- Includes urban macro, urban micro, rural, and indoor channel models.
- Supports frequencies up to 100 GHz.

The Python implementation to model the 3GPP TR 38.901 channel for wireless communication code focuses on the Urban Macrocell (UMa) and Urban Microcell (UMi) path loss and fading models. The implementation includes:

- Path Loss Calculation for LOS and NLOS scenarios.
- Doppler Shift to account for mobility.
- Small-Scale Fading using Rician and Rayleigh fading.
- Shadowing for large-scale fading.

> **IMPORTANT:**
> 1. This model is based on the papers that I shared with you and some simplifications.
> 2. This is a simple model without interference between the vehicles. The interference is a common noise added to the path loss. We can easily adapt this by considering only the vehicles that are transmitting during a given time slot and adding a correlation matrix that depends on the distances between the vehicles. It complicates the simulation a bit, but it is still feasible. Let's start with this simple model.

Below, we calculate the downlink metrics for a vehicle, including distance, path loss, fading, received power, SINR, and spectral efficiency.

For the Path Loss, we consider the 3GPP TR 38.901 Urban Macrocell (UMa) model, which includes LOS and NLOS conditions with shadowing effects.

For Doppler Shift, we have to simulate the effect of relative motion between the user and base station. This motion is calculated based on user velocity, angle (not considered here), and carrier frequency.

We assume small-scale fading by considering Rician Fading (Used for LOS conditions) and Rayleigh Fading (Used for NLOS conditions).

**Simulation Parameters:**

The outputs should be the path loss, fading gain, Doppler shift, and received power for each user.

Hereafter, the mathematical formulation of each of the considered models.

---

#### 1. Distance Calculation

The Euclidean distance *d* between the vehicle and the base station is given by:

$d = \sqrt{(x_{\text{BS}} - x_{\text{UE}})^2 + (y_{\text{BS}} - y_{\text{UE}})^2}$

where $(x_{BS}, y_{BS})$ is the base station position, and $(x_{UE}, y_{UE})$ is the vehicle position.

---

#### 2. Path Loss

The path loss for **LOS** (*Line-of-Sight*) is given by:

$PL_{\text{LOS}} = 32.4 + 20 \log_{10}(d) + 20 \log_{10}(f_{\text{GHz}})$

For **NLOS** (*Non-Line-of-Sight*), an additional penalty is added:

$PL_{\text{NLOS}} = PL_{\text{LOS}} + \text{NLOS Penalty}$

where:
- $d$: Distance (meters)
- $f_{\text{GHz}}$: Carrier frequency in GHz

---

#### 3. Shadowing

Shadowing is modeled as a Gaussian random variable with standard deviation $\sigma$:

$PL = PL_{\text{LOS/NLOS}} + N(0, \sigma^2)$

---

#### 4. Fading (Rician)

Rician fading for LOS is generated as:

$\text{Fading} = \sqrt{\frac{K}{K+1}} + N(0, \sigma^2)$

For NLOS, Rayleigh fading is used.

---

#### 5. Received Power

The received power $P_{\text{RX}}$ is computed as:

$P_{\text{RX}} = P_{\text{TX}} - PL + 10 \log_{10}(\text{Fading}^2)$

where:
- $P_{\text{TX}}$: Transmit power in dBm
- $PL$: Path loss (dB)
- $Fading$: Fading gain

---

#### 6. Signal-to-Interference-plus-Noise Ratio (SINR)

$\text{SINR} = 10^{\frac{P_{\text{RX}} - N_0}{10}}$

where $N_0$ is the noise power, computed as:

$N_0 = -174 + 10 \log_{10}(BW)$

where $BW$ is the bandwidth (Hz).

---

#### 7. Spectral Efficiency

The spectral efficiency $SE$ is calculated using the Shannon formula:

$SE = \log_2(1 + \text{SINR})$

### Generate raw communication (around 4 minutes):

```bash
source scripts/run/raw/communication.sh
```
Expected output: 
```bash
index  25
processing mobility file  1
index  25
processing mobility file  3
index  25
processing mobility file  4
index  25
processing mobility file  0
processing mobility file  8
index  25
```

### Generate processed communication (< 30 seconds):

Now, we take all the throughput files and take the average, which will be used on the simulator. Each client has its average throughput that depends on their distance to the base station.
```bash
source scripts/run/processed/communication.sh
```
Expected output: 
```bash
processing file  3
processing file  5
processing file  0
processing finished
processing finished
processing finished
```

### Generate delay results (< 30 seconds):

This script selects the clients and generates the communication delay result for different algorithms. The output allows us to analyze the results obtained on the paper.
```bash
python src/main.py
```
Expected output: 
```bash
processing model size  500  dataset  8
processing model size  500  dataset  8
processing model size  500  dataset  8
processing model size  500  dataset  8
processing model size  500  dataset  9
processing model size  500  dataset  9
processing model size  500  dataset  9
processing model size  500  dataset  9
processing model size  500  dataset  9
experiments finished
```


The previous python script generates several CSV files, which must be aggregated to be consumed. This can be done by executing the following script:
```bash
python process_results/aggregate_individual_results.py
```


Another process that we should do is the delays per epoch, to show on the graphs:
```bash
python process_results/process_epoch.py
```

Let's execute a federated learning training during 3 epochs with our 5 clients. Let's select 2 clients per epoch. We need to run with both datasets, so this experiment takes around 5 minutes. If you are running on a virtual machine, the time can be way longer due to the dataset pre-processing. Therefore, we recommend skipping directly to the [Results](#results) Section using the already generated data in this repository.
```bash
source scripts/run/training.sh
```

We need to process the results to generate the figure (< 1 second):
```bash
python process_results/accuracy.py
```

We also need to generate the energy consumption regarding the number of client failures. 

```bash
python src/energy_consumption.py
```

This script generates the results located in results/energy.

# Results

## Training Time Figure
```bash
python generate_figures/communication.py
```
The script generates the results located in figures/communication\_model\_sizesize\_500\_pt.png

## Epoch time figure: 

```bash
python generate_figures/epoch_delays.py
```
This script generates the results located in figures/time\_epoch2\_pt.png and figures/time\_epoch5\_pt.png

## Accuracy Figure
```bash
python generate_figures/accuracy.py
```

## Energy figure

```bash
python generate_figures/energy.py
```
This script generates the results located on figures/training\_efficiency\_pt.png.

# Paper

[TOFL: Time Optimized Federated Learning](https://www.gta.ufrj.br/ftp/gta/TechReports/SSA25.pdf)

# Cite this work

```bash
@inproceedings{souza2025tofl,
  title={TOFL: Time Optimized Federated Learning},
  author={de Souza, L. A. C., Sammarco, M., Achir, N., Campista, M. E. M., Costa, L. H. M. K.},
  booktitle={XXV Simpósio Brasileiro de Cibersegurança (SBSeg)},
  year={2025},
  organization={SBC}
}
```

# LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

