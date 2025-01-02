# Project for "Architecture of Advanced Computers and Accelerators" Course, ECE AUTh
# Part 1
### 1 Specifications based on the file starter_se.py

With the execution of the following command, the type of the CPU is defined through the `--cpu` flag. So the minorCPU model is used in this simulation. 
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
The `config.ini` file contains configuration settings for the system, which are divided into sections. The primary difference with the `config.json` lies in format and usage. A `.json` file provides a hierarchical structure.

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
The stats.txt file contains the following values:
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

$$L2_{accesses} =  L1I_{misses} + L1D_{misses} - L1_{shared\_hits} = 327 + 177 - 30 = 474$$
### 3 Models of in-order CPUs
##### SimpleCPU
The **SimpleCPU** is a functional, in-order model suitable for cases where detailed models are not needed. It is divided in three classes: **BaseSimpleCPU**, **AtomicSimpleCPU** and **TimingSimpleCPU**.
- **BaseSimpleCPU** manages architected state, shared stats, common functions (e.g., interrupt checks, fetch requests, execution setup/actions, PC advancement), and implements the ExecContext interface. The **BaseSimpleCPU** provides a shared foundation for the **AtomicSimpleCPU** and **TimingSimpleCPU** by encapsulating the common functionality and state they both require.
- **AtomicSimpleCPU** uses atomic memory accesses which are faster than detailed access. It estimates the total cache access time using the latency estimates from the atomic accesses.
- **TimingSimpleCPU** uses timing memory accesses, emphasizing accurate memory timing interactions. It waits for the memory system to respond (success or nack) before continuing, stalling on cache accesses.
##### Trace CPU
The **Trace CPU** does not belong either in in-order or out-of-order models, because it plays back recorded traces without carrying out commands dynamically. The trace data determines its behavior which is created based on the dependencies between loads and stores.
##### Minor CPU Model
The **MinorCPU** is an in-order processor model with a fixed, configurable pipeline designed for in-order execution. It has four pipeline stages (Fetch1, Fetch2, Decode, Execute). These stages are connected through buffers to handle inter-stage delays and branch predictions. It provides effective management of memory access, branch prediction, and pipeline activity while avoiding complicated data structures and concentrating on dynamic instruction data. **MinorCPU** allows detailed customization of parameters while optimizing performance by skipping idle cycles. Although this model does not support multithreading, the model is ideal for microarchitectural studies of simple in-order processors. 
##### HPI
The **HPI (High-Performance In-order)** is a modern in-order Armv8-A implementation.
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

| Simulation time in ms | DDR3  | DDR4  |
| --------------------- | ----- | ----- |
| MinorCPU              | 0.054 | 0.053 |
| TimingSimpleCPU       | 0.079 | 0.078 |

Changing to a better memory technology we observe a slight improvement. Since the program has limited data and therefore the memory accesses are also limited the difference is not noticeable.
