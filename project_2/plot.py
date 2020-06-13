import matplotlib.pyplot as plt
import defines as df
import numpy as np

averages = np.loadtxt('averages_'+df.configs+'.txt', dtype=np.float, delimiter='\n')
maxs = np.loadtxt('maxs_'+df.configs+'.txt', dtype=np.float, delimiter='\n')
mins = np.loadtxt('mins_'+df.configs+'.txt', dtype=np.float, delimiter='\n')

fig, ax = plt.subplots()
ax.plot(range(df.max_generations+1), averages, '-')
ax.plot(range(df.max_generations+1), mins, '-', color="#011254")
ax.plot(range(df.max_generations+1), maxs, '-', color="#0294dd")
ax.fill_between(range(df.max_generations+1), mins, maxs, alpha=0.2)
plt.show()
