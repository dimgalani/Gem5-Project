# Project for "Architecture of Advanced Computers and Accelerators" Course, ECE AUTh
# Part 1
### 1 Specifications based on the file starter_se.py

With the execution of the following command, the type of the CPU is defined through the `--cpu` flag. So, the minorCPU model is used in this simulation. 
```bash
./build/ARM/gem5.opt -d hello_result configs/example/arm/starter_se.py --cpu="minor" "tests/test-progs/hello/bin/arm/linux/hello"
```

According to the main function, the default values are passed to the other specifications since no explicit values were given. Key parameters passed on the gem5:

- **CPU Frequency: 1GHz**
```python
parser.add_argument("--cpu-freq", type=str, default="1GHz")
```

- **Number of Cores: 1**
```python
    parser.add_argument("--num-cores", type=int, default=1,
                        help="Number of CPU cores")
```

- **Memory Type: DDR3_1600_8x8**
```python
    parser.add_argument("--mem-type", default="DDR3_1600_8x8",
                        choices=ObjectList.mem_list.get_names(),
                        help = "type of memory to use")
```

- **Number of Memory Channels: 2**
```python
    parser.add_argument("--mem-channels", type=int, default=2,
                        help = "number of memory channels")
```

- **Number of Memory Ranks per Channel: None**
```python
    parser.add_argument("--mem-ranks", type=int, default=None,
                        help = "number of memory ranks per channel")
```

- **Physical Memory Size: 2GB**
```python
    parser.add_argument("--mem-size", action="store", type=str,
                        default="2GB",
                        help="Specify the physical memory size")
```

Some other characteristics of the system are defined through the initialization of the class Object SimpleSeSystem. Such as:

- **System Voltage Domain: 3.3V**
```python
self.voltage_domain = VoltageDomain(voltage="3.3V")
```

- **System Clock Domain: 1GHz**

```python
        self.clk_domain = SrcClockDomain(clock="1GHz",
                                         voltage_domain=self.voltage_domain)
```

- **Voltage of the CPU Clusters: 1.2V**
```python
        self.cpu_cluster = devices.CpuCluster(self,
                                              args.num_cores,
                                              args.cpu_freq, "1.2V",
                                              *cpu_types[args.cpu])
```

- **Cache Line Size: 64**
```python
    # Use a fixed cache line size of 64 bytes
    cache_line_size = 64
```

### 2 Understanding the config.ini and config.json files
#### a) Verification of the 1st question's assumptions
The `config.ini` file contains configuration settings for the system, which are divided into sections. The primary difference with the `config.json` lies in format and usage. A `.json` file provides a hierarchical structure. Bellow there are the lines with the specifications that were found on the `ini` file first, followed by the ones at the `json` file.

- **CPU Type: MinorCPU**

```ini
66    [system.cpu_cluster.cpus]
67    type=MinorCPU
```


```
153	 "cpus": [
154	    {
439	      "type": "MinorCPU",
```

- **CPU Frequency: 1GHz**
```ini
58    [system.cpu_cluster.clk_domain]
59    type=SrcClockDomain
60    clock=1000
```

```
4   "system": {
127     "cpu_cluster": {
140          "clk_domain": {
142            "clock": [
143                1000
144            ],
```

-  **Number of Cores: 1**
```ini
66    [system.cpu_cluster.cpus]
72    cpu_id=0
``` 

```
4   "system": {
127     "cpu_cluster": {
153          "cpus": [
154              {
431                "cpu_id": 0,
```

There is just one core because there is only one CPU in the cpu_cluster with cpu_id=0.

- **Memory Type: DDR3_1600_8x8**
On the `config.dot` image:
![Pasted image 20250101031640](https://github.com/user-attachments/assets/d5264c97-d471-47ef-8f36-c4560d3541bf)


- **Number of memory channels: 2**
```ini
11    [system]
26    memories=system.mem_ctrls0 system.mem_ctrls1
```

```
4   "system": {
66      "memories": [
67          "system.mem_ctrls0",
68          "system.mem_ctrls1"
69        ],
```
There are two memory channels the mem_ctrls0 and the mem_ctrls1.

- **Number of memory ranks per channel: 2**
```ini
1236  [system.mem_ctrls0]
1296  ranks_per_channel=2
.
1327  [system.mem_ctrls1]
1387  ranks_per_channel=2
```

```
1710	 "mem_ctrls": [
1711	     {
1771			"ranks_per_channel": 2,
1825		 },
1826		 {
1886			 "ranks_per_channel": 2,
1940		 }],
```

Although on the starter_se.py the ranks per channel were initialized as none, on the `config.ini` file the ranks per channel are equal to two.

- **Physical memory size: 2GB**

`2 GiB = 2147483648 bytes`

```ini
11   [system]
25   mem_ranges=0:2147483647
```

```
4   "system": {
84        "mem_ranges": [
85            "0:2147483647"
86        ],
```

- **System Voltage Domain: 3.3V**
```ini
1450    [system.voltage_domain]
1451    type=VoltageDomain
1452    eventq_index=0
1453    voltage=3.3
```

```
4   "system": {
102        "voltage_domain": {
103            "name": "voltage_domain",
104           "eventq_index": 0,
105            "voltage": [
106                3.3
107            ],
108            "cxx_class": "VoltageDomain",
109            "path": "system.voltage_domain",
110            "type": "VoltageDomain"
111        },
```

- **System Clock Domain: 1GHz**
```ini
44    [system.clk_domain]
45    type=SrcClockDomain
46    clock=1000
```

```
4   "system": {
71        "clk_domain": {
72            "name": "clk_domain",
73            "clock": [
74                1000
75            ],
```

- **Voltage of the CPU Clusters: 1.2V**
```ini
1223    [system.cpu_cluster.voltage_domain]
1224    type=VoltageDomain
1225    eventq_index=0
1226    voltage=1.2
```

```
4   "system": {
127        "cpu_cluster": {
128            "name": "cpu_cluster",
130            "voltage_domain": {
133                 "voltage": [
134                     1.2
135                 ],
```

- **Cache Line Size: 64**
```ini
11   [system]
15   cache_line_size=64
```

```
4   "system": {
112     "cache_line_size": 64,
```

#### b) Simulation Statistics (sim_seconds, sim_insts and host_inst_rate)
The `stats.txt` file [^1] contains the following values:
- sim_seconds = 0.000035 = 35 μs, total simulated time for the simulation.
- sim_insts = 5027, total number of instructions committed by the CPU.
- host_inst_rate = 76338 instructions/sec, rate that the simulator executes the instructions.
#### c) Commited Instructions
```text
sim_insts                                        5027                       # Number of instructions simulated
system.cpu_cluster.cpus.committedInsts           5027                       # Number of instructions committed
system.cpu_cluster.cpus.committedOps             5831                       # Number of ops (including micro ops) committed
```

The total number of instructions `sim_insts` matches the total number of committed instructions `system.cpu_cluster.cpus.committedInsts`. In some scenarios, they could not be aligned due to speculative execution, e.g., on branch predictions, some instructions are discarded later.
In addition, `committedOps` represents the actual low-level operations executed by the CPU, including micro-operations, which are smaller tasks created by breaking down complex instructions (e.g., floating-point operations or memory accesses). Therefore, it is expected the number of committed operations to exceed that of committed instructions.

#### d) Accesses on the L2 cache
The total number of accesses on the L2 cache can be found in the following line.
```text
system.cpu_cluster.l2.overall_accesses::total          474                       # number of overall (read+write) accesses
```

Additionally, the times that the L2 cache was accessed can be calculated through the sum of the misses of the L1 cache. The L1  cache is separated into icache (instruction cache) and dcache (data cache).

```
system.cpu_cluster.cpus.icache.overall_misses::total          327                       # number of overall misses
system.cpu_cluster.cpus.dcache.overall_misses::total          177                       # number of overall misses
system.cpu_cluster.cpus.dcache.overall_mshr_hits::total           30                       # number of overall MSHR hits
```

 However, according to the statistics, 327+177 equals 504 accesses. Since this number does not align with the L2 overall accesses, it was assumed that these requests were resolved elsewhere, e.g. on the shared files, without accessing the L2 cache. On the dcache shared files there are 30 hits. So the correct equation is:

$$L2_{accesses} =  L1I_{misses} + L1D_{misses} - L1_{shared\textunderscore hits} = 327 + 177 - 30 = 474$$
### 3 Models of in-order CPUs
##### SimpleCPU
The **SimpleCPU** is a functional, in-order model suitable for cases where detailed models are not needed. It is divided in three classes: **BaseSimpleCPU**, **AtomicSimpleCPU** and **TimingSimpleCPU**. [^2]
- **BaseSimpleCPU** manages architected state, shared stats, common functions (e.g., interrupt checks, fetch requests, execution setup/actions, PC advancement), and implements the ExecContext interface. The **BaseSimpleCPU** provides a shared foundation for the **AtomicSimpleCPU** and **TimingSimpleCPU** by encapsulating the common functionality and state they both require.
- **AtomicSimpleCPU** uses atomic memory accesses which are faster than detailed access. It estimates the total cache access time using the latency estimates from the atomic accesses.
- **TimingSimpleCPU** uses timing memory accesses, emphasizing accurate memory timing interactions. It waits for the memory system to respond (success or nack) before continuing, stalling on cache accesses. [^5]
##### Trace CPU
The **Trace CPU** does not belong either in in-order or out-of-order models, because it plays back recorded traces without carrying out commands dynamically. The trace data determines its behavior which is created based on the dependencies between loads and stores. [^3]
##### Minor CPU Model
The **MinorCPU** is an in-order processor model with a fixed, configurable pipeline designed for in-order execution. It has four pipeline stages (Fetch1, Fetch2, Decode, Execute). These stages are connected through buffers to handle inter-stage delays and branch predictions. It provides effective management of memory access, branch prediction, and pipeline activity while avoiding complicated data structures and concentrating on dynamic instruction data. **MinorCPU** allows detailed customization of parameters while optimizing performance by skipping idle cycles. Although this model does not support multithreading, the model is ideal for microarchitectural studies of simple in-order processors. [^4]
##### HPI
The **HPI (High-Performance In-order)** is a modern in-order Armv8-A implementation. [^5]
#### a) Fibonacci sequence program
A simple program was implemented which calculates the first 40 terms of the Fibonacci sequence, without recursion, in order to be light-weighted. This program was executed twice on the gem5 using the **TimingSimpleCPU** and **MinorCPU** models.
#### b) Results

| Metric          | MinorCPU | TimingSimpleCPU |
| --------------- | -------- | --------------- |
| final_tick      | 54381000 | 78970000        |
| host_mem_usage  | 678752   | 674144          |
| host_seconds    | 0.14     | 0.03            |
| sim_insts       | 34562    | 34435           |
| sim_ops         | 40196    | 39781           |
| sim_seconds(ms) | 0.054    | 0.079           |

As expected the simulation on the MinorCPU was faster, since it uses mechanisms for optimization such as cycle skipping. In contrast with the TimingSimpleCPU where the program is blocked until the respond from the memory system.
On the other hand, the time that the program elapsed on the host is greater in the case of the MinorCPU. This can be explained through the complexity of this model. It is more computationally expensive for the host to emulate all the pipeline logic and the behavior of the MinorCPU.

#### c) Changing the frequency and the memory technology

| Simulation time in ms | 0.5GHz | 1GHz  | 5GHz  |
| --------------------- | ------ | ----- | ----- |
| MinorCPU              | 0.063  | 0.054 | 0.049 |
| TimingSimpleCPU       | 0.085  | 0.079 | 0.074 |

As the simulated CPU frequency increases, the CPU can process more ticks per second, reducing the overall simulation time.  The **MinorCPU** benefits more from this increase compared to the simpler **TimingSimpleCPU**.

| Simulation time in ms | DDR3_1600_8x8  | DDR4_2400_8x8  |
| --------------------- | ----- | ----- |
| MinorCPU              | 0.054 | 0.053 |
| TimingSimpleCPU       | 0.079 | 0.078 |

Changing to a better memory technology we observe a slight improvement. Since the program has limited data and therefore the memory accesses are also limited the difference is not noticeable.

# Part 2
## 1 Execution of SPEC CPU2006 Benchmarks on gem5
### 1 Cache Specifications
After executing the benchmarks, the following specifications were found on the `config.ini` file.

```ini
[system]
cache_line_size=64

[system.cpu.dcache]
assoc=2
size=65536

[system.cpu.icache]
assoc=2
size=32768

[system.l2]
assoc=8
size=2097152
```

|        Cache Specifications        |     Value     |
| :--------------------------------: | :-----------: |
|         L1 Data cache size         | 65536 = 64kB  |
|    L1 Data cache associativity     |       2       |
|     L1 Instruction cache size      | 32768 = 32kB  |
| L1 Instruction cache associativity |       2       |
|           L2 cache size            | 2097152 = 2MB |
|       L2 cache associativity       |       8       |
|          cache_line_size           |      64       |

### 2 Performance Metrics

Based on the `stats.txt` file:

|            Metric            |   bzip   |   mcf    |  hmmer   |   sjeng   | libm     |
| :--------------------------: | :------: | :------: | :------: | :-------: | -------- |
|     Simulation time(ms)      |  83.982  |  64.955  |  59.396  |  513.528  | 174.671  |
| CPI (cycles per instruction) | 1.679650 | 1.299095 | 1.187917 | 10.270554 | 3.493415 |
|    L1 icache missrate(%)     |  0.0077  |  2.3612  |  0.0221  |   0.002   | 0.0094   |
|    L1 dcache missrate(%)     |  1.4798  |  0.2108  |  0.1637  |  12.1831  | 6.0972   |
|     L2 cache missrate(%)     | 28.2163  |  5.5046  |  7.776   |  99.9972  | 99.9944  |
|   system.clk_domain.clock    |   1000   |   1000   |   1000   |   1000    | 1000     |
| cpu_cluster.clk_domain.clock |   500    |   500    |   500    |    500    | 500      |

![Figure_2](https://github.com/user-attachments/assets/aabf3fa8-1420-4179-af27-54dcbbabafea)

Based on these statistics the **sjeng** benchmarks had the highest execution time. Most likely this is caused due to the high percentages in L1 dcache misses and the L2 misses, indicating poor data locality and frequent accesses to main memory. The same applies also on libm banchmark. Also, the frequency of the CPU is 2GHz based on the ticks of cpu_cluster.clk_domain.clock. 

### 3 Trying different cpu clock
|                             | 1GHz | 2GHz | 3GHz |
| :-------------------------: | :--: | :--: | :--: |
|   system.clk_domain.clock   | 1000 | 1000 | 1000 |
| system.cpu_clk_domain.clock | 1000 | 500  | 333  |

We observe that only the system CPU clock changed when the frequency was altered. The `system.clk_domain` is used for slower, system-wide components like the memory bus `membus` and memory controllers `mem_ctrls`, as stated in the `config.json` file. They are responsible for the communication within the system and the synchronization of the components.

On the other hand, the `system.cpu_clk_domain` is used for high-performance components directly involved in the CPU's operation, including:
- CPU (`cpu`)
- Instruction and Data Caches (`icache` and `dcache`)
- Translation Lookaside Buffers: Instruction TLB (`itb`) and Data TLB (`dtb`)
- L2 Cache (`l2`)
- CPU-to-L2 Bus (`tol2bus`)

If another processor is added, it is expected to work using the same `system.clk_domain.clock` clock but with a separate CPU clock that may differ from the current processor's.



|                            |  bzip   |   mcf   |  hmmer  |  sjeng  | libm    |
| :------------------------: | :-----: | :-----: | :-----: | :-----: | ------- |
| Execution time in 1GHz(ms) | 161.025 | 127.942 | 118.530 | 704.056 | 262.327 |
| Execution time in 2GHz(ms) | 83.982  | 64.955  | 59.396  | 513.528 | 174.671 |
| Execution time in 3GHz(ms) | 58.385  | 43.867  | 39.646  | 449.821 | 146.433 |


Higher frequency leads to reduced execution times across all benchmarks. However, the scaling is not perfectly linear, because the execution time is influenced by several factors. The benchmarks with efficient cache utilization and lower CPI, like **bzip** and **hmmer**, scale better with frequency. Also, the speedup from 2GHz to 3GHz is smaller, possibly due to the workload that is inherently serial or the existence of dependencies.

### 4 Changing memory configuration

Executing the specbzip benchmark with memory type DDR3_2133_8x8 instead of DDR3_1600_x64 there is a slight improvement in the execution time and the CPI. This result was expected because the new memory type has a quicker clock.

|                              | DDR3_1600_x64 | DDR3_2133_8x8 |
| ---------------------------- | ------------- | ------------- |
| Execution time(ms)           | 83.982        | 83.609        |
| CPI (cycles per instruction) | 1.679650      | 1.672175      |

## 2 Design Exploration
The goal of this step is to optimize the CPI by modifying the following parameters:
- L1 instruction cache size 
- L1 instruction cache associativity 
- L1 data cache size 
- L1 data cache associativity 
- L2 cache size 
- L2 cache associativity 
- size cache line

But there are some limitations we must consider:
- $L1_{icache} + L1_{dcache} < 256KB$
- $L2_{cache} <4MB$


![cpi_bzip](https://github.com/user-attachments/assets/4c3737cd-0d8f-4eb2-92c2-5c779c220215)
![cpi_hmmer](https://github.com/user-attachments/assets/162744ea-09d9-4aff-814f-b325bc5aef7d)
![cpi_libm](https://github.com/user-attachments/assets/e35b4a61-4364-453a-bef5-cffa3f2e2fc2)
![cpi_mcf](https://github.com/user-attachments/assets/88443b9f-29b8-42a1-83c2-77ae5d6bfc97)
![cpi_sjeng](https://github.com/user-attachments/assets/7f54c40a-1b4a-4d6f-a010-8bb422c95902)


Several specification adjustments were made based on the initial simulation statistics and the following principles, in order to achieve a lower CPI.
- Increasing the cache size could lead to reduced miss rates, since more data or instructions can be stored locally.
- Generally, higher associativity reduces cache conflicts, especially in workloads that reuse a lot of data. However, it can also cause an increase in CPI due to complexity in accessing and managing the cache.
- A larger cache line size improves performance for workloads with good spatial locality by minimizing cache misses during sequential data access.

The following table shows the parameters of each execution, the CPI, and the cost for each change, which is used at the next step.

|                   | L1D size | L1D assoc | L1i size | L1i assoc | L2 size | L2 assoc | cache_line_size | CPI          | Cost        |
| ----------------- | -------- | --------- | -------- | --------- | ------- | -------- | --------------- | ------------ | ----------- |
| specbzip_default  | 64       | 2         | 32       | 2         | 2       | 8        | 64              | 1.610247     | 10.1048     |
| specbzip_0        | 128      | 4         | 32       | 2         | 4       | 8        | 128             | 1.556298     | 14.5899     |
| specbzip_1        | 128      | 4         | 32       | 2         | 4       | 16       | 128             | 1.555648     | 17.9914     |
| specbzip_2        | 64       | 4         | 64       | 4         | 4       | 16       | 128             | 1.555529     | 17.3765     |
| specbzip_3        | 64       | 4         | 64       | 4         | 4       | 8        | 64              | 1.580758     | 13.8750     |
| specbzip_4        | 128      | 4         | 64       | 4         | 4       | 16       | 64              | 1.580604     | 19.2765     |
| specbzip_5    | 128  | 4     | 64   | 4     | 4   | 8    | 128         | 1.556297 | 15.9750 |
| specbzip_6        | 128      | 4         | 64       | 4         | 4       | 16       | 128             | 1.555529     | 19.3765     |
| specbzip_7        | 128      | 8         | 64       | 4         | 4       | 16       | 128             | 1.547384     | 20.5237     |
| specbzip_8        | 128      | 8         | 64       | 8         | 4       | 16       | 128             | 1.547359 | 21.6709     |
| specbzip_9        | 64       | 4         | 32       | 2         | 2       | 8        | 64              | 1.594676     | 10.4899     |
| specmcf_default   | 64       | 2         | 32       | 2         | 2       | 8        | 64              | 1.279422     | 10.1048     |
| specmcf_0         | 128      | 4         | 32       | 2         | 2       | 8        | 64              | 1.278152     | 12.4899     |
| specmcf_1         | 64       | 4         | 64       | 4         | 2       | 8        | 64              | 1.138580     | 11.8750     |
| specmcf_2         | 128      | 4         | 128      | 4         | 2       | 8        | 64              | 1.137877     | 15.8750     |
| specmcf_3         | 128      | 4         | 128      | 4         | 4       | 8        | 64              | 1.137721     | 17.8750     |
| specmcf_4         | 128      | 4         | 128      | 4         | 4       | 16       | 64              | 1.137721     | 21.2765     |
| specmcf_5         | 128      | 4         | 128      | 4         | 4       | 8        | 128             | 1.111239     | 17.9750     |
| specmcf_6     | 64   | 4     | 128  | 4     | 4   | 8    | 128         | 1.111918 | 15.9750 |
| specmcf_7         | 64       | 4         | 128      | 4         | 4       | 16       | 128             | 1.111918     | 19.3765     |
| spechmmer_default | 64       | 2         | 32       | 2         | 2       | 8        | 64              | 1.185304     | 10.1048     |
| spechmmer_0       | 64       | 4         | 32       | 2         | 2       | 8        | 64              | 1.185128     | 10.4899     |
| spechmmer_1       | 64       | 8         | 32       | 2         | 2       | 8        | 64              | 1.185082     | 11.6370     |
| spechmmer_2       | 128      | 8         | 32       | 2         | 2       | 8        | 64              | 1.182809     | 13.6370     |
| spechmmer_3   | 128  | 4     | 32   | 2     | 2   | 8    | 128         | 1.178793 | 12.5899 |
| spechmmer_4       | 128      | 4         | 32       | 2         | 4       | 8        | 128             | 1.178793     | 14.5899     |
| spechmmer_5       | 128      | 4         | 64       | 4         | 4       | 8        | 128             | 1.178125     | 15.9750     |
| spechmmer_6       | 128      | 4         | 128      | 4         | 4       | 8        | 128             | 1.178110 | 17.9750     |
| spechmmer_7       | 128      | 4         | 128      | 4         | 4       | 16       | 128             | 1.178110     | 21.3765     |
| spechmmer_8       | 64       | 4         | 64       | 4         | 4       | 16       | 128             | 1.179548     | 17.3765     |
| specsjeng_default | 64       | 2         | 32       | 2         | 2       | 8        | 64              | 7.040561     | 10.1048     |
| specsjeng_0       | 64       | 4         | 32       | 2         | 2       | 8        | 64              | 7.040561     | 10.4899     |
| specsjeng_1       | 128      | 4         | 32       | 2         | 2       | 8        | 64              | 7.040599     | 12.4899     |
| specsjeng_2       | 128      | 8         | 32       | 2         | 2       | 8        | 64              | 7.040561     | 13.6370     |
| specsjeng_3       | 64       | 4         | 64       | 4         | 2       | 8        | 64              | 7.039166     | 11.8750     |
| specsjeng_4   | 64   | 4     | 32   | 2     | 2   | 8    | 128         | 4.974696 | 10.5899 |
| specsjeng_5       | 64       | 4         | 32       | 2         | 4       | 8        | 128             | 4.974696     | 12.5899     |
| specsjeng_6       | 64       | 4         | 32       | 2         | 4       | 16       | 128             | 4.974347     | 15.9914     |
| specsjeng_7       | 64       | 8         | 32       | 2         | 4       | 16       | 128             | 4.974354     | 17.1386     |
| specsjeng_8       | 64       | 4         | 128      | 4         | 4       | 16       | 128             | 4.972141 | 19.3765     |
| speclibm_default  | 64       | 2         | 32       | 2         | 2       | 8        | 64              | 2.623265     | 10.1048     |
| speclibm_0        | 64       | 4         | 32       | 2         | 2       | 8        | 64              | 2.623265     | 10.4899     |
| speclibm_1        | 128      | 8         | 32       | 2         | 2       | 8        | 64              | 2.623265     | 13.6370     |
| speclibm_2        | 64       | 4         | 64       | 4         | 2       | 8        | 64              | 2.623265     | 11.8750     |
| speclibm_3        | 64       | 4         | 32       | 2         | 4       | 8        | 64              | 2.620756     | 12.4899     |
| speclibm_4        | 64       | 4         | 32       | 2         | 4       | 8        | 128             | 1.989132     | 12.5899     |
| speclibm_5        | 64       | 4         | 32       | 2         | 4       | 16       | 128             | 1.989132     | 15.9914     |
| speclibm_6        | 64       | 4         | 32       | 2         | 2       | 8        | 128             | 1.990458     | 10.5899     |
| speclibm_7        | 64       | 2         | 32       | 2         | 2       | 8        | 128             | 1.990458     | 10.2048     |
| speclibm_8    | 64   | 2     | 32   | 2     | 4   | 8    | 128         | 1.989132 | 12.2048 |

### 3 Cost of performance optimization
The specification change introduces some tradeoffs even though it improves certain performance metrics. Therefore, it is useful to create a cost function to evaluate the impact of these changes.
Since latency and throughput are both critical for L1 cache performance, L1icache and L1dcache are typically selected to have sizes ranging from a few decades of KB to a hundreds of KB. For this reason, the L1 cache technology is more expensive **per byte**, while the L2 cache is much larger and contributes significantly to chip space. In this way, we can state that an L1 32kB cache (either icache or dcache) contributes one unit to the cost function, which is equivalent to 1MB of L2 cache. [^6] [^8]

$$cost_{L1\textunderscore size} = \dfrac{size}{32kB},\hspace{0.75em} cost_{L2\textunderscore size} = \dfrac{size}{1MB}$$

The increase of the associativity has a smaller effect on cost than the cache size. Similar due to the strict speed and power requirements of the L1, the increase of the associativity of the L1 has a greater impact in contrast with the L2. Additionally, there is a non-linear dependence between the cost and the associativity. Doubling from 4-way to 8-way is more expensive than going from 2-way to 4-way, and beyond 8-way or 16-way, the added cost often outweighs the benefits.[^8] This behavior is being portrayed by the following terms

$$cost_{L1\textunderscore  assoc} = e^{0.13 \cdot assoc},\hspace{0.75em}cost_{L2\textunderscore assoc} = e^{0.11 \cdot assoc}$$

The cache line size has a minor impact on the cost, because it just changes the arrangement of the blocks. The effect that has on the performance depends on the data of the benchmark. When a cache miss occurs on a smaller cache line, less data is sent to the block. However, when the cache line size is larger, there are fewer blocks, so there is less complexity. [^8] [^7] 

$$cost_{cache\textunderscore line\textunderscore size} = 0.1\cdot\dfrac{line\textunderscore size}{64bytes}$$
Altogether, the cost function is defined as:
$$cost = \dfrac{L1\textunderscore icachesize}{32kB} +\dfrac{L1\textunderscore dcachesize}{32kB}+ \dfrac{L2\textunderscore size}{1MB} + e^{0.13 \cdot L1\textunderscore dcache\textunderscore assoc} + e^{0.13 \cdot L1\textunderscore icache\textunderscore assoc} + e^{0.11 \cdot L2\textunderscore assoc} + 0.1\cdot\dfrac{line\textunderscore size}{64bytes}$$

The costs on the table above are calculated based on this cost function. We observe that in many cases achieving the best CPI comes with a significantly higher cost. Therefore, it is often preferrable to compromise on the performance to keep the cost affordable. Finally, by balancing cost and CPI, the optimal parameters for each specification are:

|                 | L1D size | L1D assoc | L1i size | L1i assoc | L2 size | L2 assoc | cache_line_size | CPI          | Cost        |
| --------------- | -------- | --------- | -------- | --------- | ------- | -------- | --------------- | ------------ | ----------- |
| specbzip_5  | 128  | 4     | 64   | 4     | 4   | 8    | 128         | 1.556297 | 15.9750 |
| specmcf_6   | 64   | 4     | 128  | 4     | 4   | 8    | 128         | 1.111918 | 15.9750 |
| spechmmer_3 | 128  | 4     | 32   | 2     | 2   | 8    | 128         | 1.178793 | 12.5899 |
| specsjeng_4 | 64   | 4     | 32   | 2     | 2   | 8    | 128         | 4.974696 | 10.5899 |
| speclibm_8  | 64   | 2     | 32   | 2     | 4   | 8    | 128         | 1.989132 | 12.2048 |

[^1]: https://www.gem5.org/documentation/learning_gem5/part1/gem5_stats/
[^2]: https://www.gem5.org/documentation/general_docs/cpu_models/SimpleCPU
[^3]: https://www.gem5.org/documentation/general_docs/cpu_models/TraceCPU
[^4]: https://www.gem5.org/documentation/general_docs/cpu_models/minor_cpu
[^5]: https://stackoverflow.com/questions/58554232/what-is-the-difference-between-the-gem5-cpu-models-and-which-one-is-more-accurat
[^6]: https://stackoverflow.com/questions/4666728/why-is-the-size-of-l1-cache-smaller-than-that-of-the-l2-cache-in-most-of-the-pro
[^7]: Przybylski, Steven A.. Cache and Memory Hierarchy Design: A Performance Directed Approach. USA, Elsevier Science, 2014.
[^8]: Hennessy, John L., et al. Computer Architecture: A Quantitative Approach. India, Elsevier Science, 2006.
