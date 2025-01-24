from pickle import load
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))

for index in range(10):
    with open("results/7000/results_client"+str(index),"rb") as loader:
        result = load(loader)
        plt.plot(range(101),result,label="client_"+str(index))

plt.xlabel("Epoch Number (#)")
plt.ylabel("Delay (s)")
plt.legend()
plt.show()