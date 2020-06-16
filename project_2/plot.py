import matplotlib.pyplot as plt
import defines as df
import numpy as np
from os import listdir


for directory in listdir('outputs/'):
    print("Plotting " + directory)

    averages = np.loadtxt('outputs/'+directory+'/averages.txt', dtype=np.float, delimiter='\n')
    maxs = np.loadtxt('outputs/'+directory+'/maxs.txt', dtype=np.float, delimiter='\n')
    mins = np.loadtxt('outputs/'+directory+'/mins.txt', dtype=np.float, delimiter='\n')


    fig, ax = plt.subplots()
    ax.plot(range(df.max_generations), maxs, '-', color="#0294dd", label='Adequação máxima')
    ax.plot(range(df.max_generations), averages, '-',color="#0e2795", label='Adequação média')
    ax.plot(range(df.max_generations), mins, '-', color="#011254", label='Adequação mínima')
    ax.fill_between(range(df.max_generations), mins, maxs, alpha=0.2)
    
    # Styling the graph
    ax.set_xlabel('Gerações')
    ax.set_ylabel('Adequação')
    plt.legend(loc='lower right')

    plt.savefig('outputs/'+directory+'/plot.png', dpi=600)
    plt.close()
