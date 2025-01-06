import matplotlib.pyplot as plt
import numpy as np

# Data
benchmarks = ["bzip", "mcf", "hmmer", "sjeng", "libm"]
sim_time = [83.982, 64.955, 59.396, 513.528, 174.671]
cpi = [1.679650, 1.299095, 1.187917, 10.270554, 3.493415]
l1_icache_missrate = [0.0077, 2.3612, 0.0221, 0.002, 0.0094]
l1_dcache_missrate = [1.4798, 0.2108, 0.1637, 12.1831, 6.0972]
l2_cache_missrate = [28.2163, 5.5046, 7.776, 99.9972, 99.9944]

# Define pastel colors
colors = {
    'blue': '#89CFF0',  
    'green': '#98FB98',  
    'red': '#ff4d4d',  
    'orange': '#ffc761',  
    'purple': '#DDA0DD'  
}
# Create plots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: sim_time per benchmark
axs[0, 0].bar(benchmarks, sim_time, color=colors['blue'])
axs[0, 0].set_title('Simulation Time per Benchmark')
axs[0, 0].set_ylabel('Simulation Time (s)')

# Plot 2: cpi per benchmark
axs[0, 1].bar(benchmarks, cpi, color=colors['green'])
axs[0, 1].set_title('CPI per Benchmark')
axs[0, 1].set_ylabel('CPI')

# Plot 3: l1_icache_missrate and l1_dcache_missrate per benchmark
x = np.arange(len(benchmarks))
width = 0.35
axs[1, 0].bar(x - width/2, l1_icache_missrate, width, label='L1 I-Cache Miss Rate', color=colors['red'])
axs[1, 0].bar(x + width/2, l1_dcache_missrate, width, label='L1 D-Cache Miss Rate', color=colors['orange'])
axs[1, 0].set_title('L1 Cache Miss Rates per Benchmark')
axs[1, 0].set_ylabel('Miss Rate (%)')
axs[1, 0].set_xticks(x)
axs[1, 0].set_xticklabels(benchmarks)
axs[1, 0].legend()

# Plot 4: l2_cache_missrate per benchmark
axs[1, 1].bar(benchmarks, l2_cache_missrate, color=colors['purple'])
axs[1, 1].set_title('L2 Cache Miss Rate per Benchmark')
axs[1, 1].set_ylabel('Miss Rate (%)')

# Adjust layout
plt.tight_layout()
plt.show()