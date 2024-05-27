# Data Collection in IoT Sensor Network Using Robots

## Overview
This project aims to implement and evaluate three algorithms for data collection in an IoT sensor network using robots: Greedy 1, Greedy 2, and MARL. The network is modeled as a graph where nodes represent sensor nodes and edges represent the communication links between them. The objective is to ensure efficient data collection with minimal energy consumption using a battery-powered robot.

## Network Model
- The IoT sensor network is represented as a graph `G(V,E)`, where `V = {1, 2, ..., N}` is the set of `N` nodes, and `E` is the set of edges.
- Sensor nodes are randomly generated within an `x` by `y` area.
- Each node has the same transmission range `Tr`. Nodes within this range can communicate directly and are connected by an edge.
- `p` nodes are randomly selected as storage-depleted data generating nodes (data nodes, DNs), denoted as `DN = {DN1, DN2, ..., DNp}`.
- Each DN has `si` number of data packets, each 400 bytes (3200 bits).
- Other nodes are storage nodes (SNs), with each `SNi` having a storage capacity of `mi` data packets.

## Energy Model
- Sensor nodes are battery-powered with limited energy.
- Communication between nodes costs battery power.
- Transmission energy spent by node `i` sending `k`-bit data to node `j` over distance `l`:
  - `ET (k, l) = Eelec * k + Eamp * k * l^2`
- Receiving energy spent by node `j` receiving `k`-bit data:
  - `ER (k) = Eelec * k`
- Constants:
  - `Eamp = 100 pJ/bit/m^2`
  - `Eelec = 100 nJ/bit`
- Edge weight (cost) for communication between nodes `i` and `j`:
  - `Cost(i, j) = 2 * Eelec * k + Eamp * k * l^2`

## Objectives
- **Connectivity Check**: Verify if the sensor network graph is connected.
  - If not, print "the network is not connected" and prompt user input again.
- **Feasibility Check**: Ensure that the network has enough storage capacity for all data packets.
  - Condition: `p * q <= (N - p) * m`
  - If not, print "there is not enough storage in the network" and prompt user input again.
- **Data Collection**: Once connectivity and feasibility are satisfied:
  - List the IDs of DNs and the number of data items each has, and the IDs of storage nodes.
  - Prompt the user to input a DN node and a storage node (SN).
  - Input the initial energy level of the robot in Joules.

## Programming Objective
1. Prompt for network parameters:
   - Width `x` and length `y` of the sensor network (default: 2000 meters x 2000 meters)
   - Number of sensor nodes `N` (default: 100)
   - Transmission range `Tr` in meters (default: 400 meters)
   - Number of DNs `p` (default: 50)
   - Maximum number of data packets each DN has `q` (default: 1000)
   - Storage capacity `m` of each storage node (assumed uniform)
   - Initial energy level `B` of the robot in Joules (default: 1,000,000)

2. Check network connectivity and feasibility.

3. List DNs and SNs, then prompt for DN and SN IDs.

4. Implement and run the algorithms:
   - **Greedy 1**
   - **Greedy 2**
   - **MARL**

5. For each algorithm, print:
   - The route the robot takes
   - The cost of the route
   - The total prizes along the route (total number of data packets collected)
   - The left budget (battery power) of the robot
   - The running time of the algorithm

## Usage
### Prerequisites
- Python 3.x
