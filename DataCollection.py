import random
import math

class Node:
    def __init__(self, node_id, x, y, capacity=0):
        self.id = node_id
        self.x = x
        self.y = y
        self.capacity = capacity

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Graph:
    def __init__(self, width, length, n, tr, p, q):
        self.width = width
        self.length = length
        self.n = n
        self.tr = tr
        self.p = p
        self.q = q
        self.nodes = []
        self.dns = []

        self.generate_nodes()
        self.check_connectivity()
    def __len__(self):
        return len(self.nodes)

    def generate_nodes(self):
        for i in range(1, self.n + 1):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.length)
            if i <= self.p:
                capacity = 0
                data_packets = random.randint(1, self.q)
                self.dns.append((i, data_packets))
            else:
                capacity = random.randint(1, self.q)
            node = Node(i, x, y, capacity)
            self.nodes.append(node)

    def check_connectivity(self):
        visited = set()
        stack = [self.nodes[0]]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend([other for other in self.nodes if node.distance(other) <= self.tr and other not in visited])
        if len(visited) != len(self.nodes):
            print("The network is not connected.")
            self.generate_nodes()
        else:
            print("\n=========================")
            print("The network is connected.")
            print("=========================")
            print("\n")
            print("\n")
            print("\nIDs of DNs and the number of data packets each has: ", end="")
            for i, dn in enumerate(self.dns):
                if i > 0:
                    print(", ", end="")
                print(f"DN{dn[0]}: {dn[1]}", end="")
            print("")

if __name__ == "__main__":
    width = input("Enter the width of the sensor network (in meters): ")
    length = input("Enter the length of the sensor network (in meters): ")
    n = input("Enter the number of sensor nodes: ")
    tr = input("Enter the transmission range of sensor nodes (in meters): ")
    p = input("Enter the number of data nodes: ")
    q = input("Enter the maximum number of data packets each DN has: ")

    graph = Graph(float(width), float(length), int(n), float(tr), int(p), int(q))

import networkx as nx
import matplotlib.pyplot as plt

# create an empty undirected graph
G = nx.Graph()

# add nodes to the graph
for node in graph.nodes:
    if node.id in [dn[0] for dn in graph.dns]:  # check if node is a datanode
        G.add_node(node.id, pos=(node.x, node.y), color='blue')  # add a different color for datanodes
    else:
        G.add_node(node.id, pos=(node.x, node.y))  # add the default color for other nodes

# add edges to the graph
for i, node1 in enumerate(graph.nodes):
    for j, node2 in enumerate(graph.nodes):
        if i < j and node1.distance(node2) <= graph.tr:
            G.add_edge(node1.id, node2.id)

# set node positions based on the x and y coordinates
pos = nx.get_node_attributes(G, 'pos')

# set node colors based on the color attribute
node_colors = nx.get_node_attributes(G, 'color')
node_colors = [node_colors[node] if node in node_colors else 'gray' for node in G.nodes()]

# draw the graph
nx.draw(G, pos, node_size=50, node_color=node_colors, with_labels=True)

# show the graph
plt.show()


initial_energy = float(input("\nEnter the initial energy level of the robot in Joules: "))

def visualize_route(graph, route):
    # create an empty directed graph
    G = nx.DiGraph()

    # add nodes to the graph
    for node in graph.nodes:
        if node.id in [dn[0] for dn in graph.dns]:  # check if node is a datanode
            G.add_node(node.id, pos=(node.x, node.y), color='blue')  # add a different color for datanodes
        else:
            G.add_node(node.id, pos=(node.x, node.y))  # add the default color for other nodes

    # add edges to the graph
    for i in range(len(route)-1):
        G.add_edge(route[i].id, route[i+1].id)

    # set node positions based on the x and y coordinates
    pos = nx.get_node_attributes(G, 'pos')

    # set node colors based on the color attribute
    node_colors = nx.get_node_attributes(G, 'color')
    node_colors = [node_colors[node] if node in node_colors else 'gray' for node in G.nodes()]

    # set edge colors based on the route
    edge_colors = ['red' if G.has_edge(route[i].id, route[i+1].id) else 'gray' for i in range(len(route)-1)]

    # draw the graph
    nx.draw(G, pos, node_size=50, node_color=node_colors, edge_color=edge_colors, with_labels=True)

    # show the graph
    plt.show()

import time

def GreedyAlgorithm1(graph, initial_energy):
    # Calculate the distance matrix between all nodes
    dist_matrix = [[node.distance(other) for other in graph.nodes] for node in graph.nodes]

    # Initialize variables
    visited = set()
    current_node = graph.nodes[0]
    route = [current_node]
    prizes = 0
    cost = 0
    energy_budget = initial_energy

    # Start timer
    start_time = time.time()

    # Visit each node exactly once
    while len(visited) < graph.n:
        # Find the nearest unvisited node
        nearest_node = None
        min_distance = float("inf")
        for node in graph.nodes:
            if node not in visited:
                distance = dist_matrix[current_node.id - 1][node.id - 1]
                if distance < min_distance:
                    nearest_node = node
                    min_distance = distance

        # Check if the nearest node is reachable with the remaining energy
        energy_consumption = min_distance * 0.002
        if energy_budget - energy_consumption < 0:
            # Not enough energy to reach the nearest node, return to node 0
            energy_consumption = dist_matrix[current_node.id - 1][0] * 0.002
            cost += dist_matrix[current_node.id - 1][0]
            energy_budget -= energy_consumption
            current_node = graph.nodes[0]
            route.append(current_node)
        else:
            # Visit the nearest node
            visited.add(nearest_node)
            prizes += nearest_node.capacity
            cost += min_distance
            energy_budget -= energy_consumption
            current_node = nearest_node
            route.append(current_node)

    # Return to node 0
    energy_consumption = dist_matrix[current_node.id - 1][0] * 0.002
    cost += dist_matrix[current_node.id - 1][0]
    energy_budget -= energy_consumption
    route.append(graph.nodes[0])

    # End timer
    end_time = time.time()
    visualize_route(graph, route)
    # Print results
    print("\nRunning Greedy Algorithm 1 :")
    print("Route:", [node.id for node in route])
    print("Cost:", cost)
    print("Total prizes:", prizes)
    print("Energy budget left:", initial_energy-energy_budget)
    print("Running time:", end_time - start_time)

# Call the function with the initialized graph and initial energy level
GreedyAlgorithm1(graph, initial_energy)




import numpy as np
import random
import time
import heapq
def GreedyAlgorithm2(graph, initial_energy):
    # Calculate the distance matrix between all nodes
    dist_matrix = [[node.distance(other) for other in graph.nodes] for node in graph.nodes]

    # Initialize variables
    visited = set()
    current_node = graph.nodes[0]
    route = [current_node]
    prizes = 0
    k=5
    cost = 0
    energy_budget = initial_energy

    # Start timer
    start_time = time.time()

    # Visit each node exactly once
    while len(visited) < graph.n:
    # Find the unvisited node with the maximum prizes/distance ratio among the nearest nodes
        max_ratio_node = None
        max_ratio = -float("inf")
        nearest_nodes = heapq.nsmallest(k, (node for node in graph.nodes if node not in visited),
                                        key=lambda node: dist_matrix[current_node.id - 1][node.id - 1])
        for node in nearest_nodes:
            distance = dist_matrix[current_node.id - 1][node.id - 1]
            if distance <= energy_budget * 500:  # Check if node is reachable with remaining energy
                if distance == 0:
                    ratio = float('inf')
                else:
                    ratio = node.capacity / distance

                if ratio > max_ratio:
                    max_ratio = ratio
                    max_ratio_node = node

        if max_ratio_node is None:
            # No reachable unvisited nodes, return to node 0
            energy_consumption = dist_matrix[current_node.id - 1][0] * 0.002
            cost += dist_matrix[current_node.id - 1][0]
            energy_budget -= energy_consumption
            current_node = graph.nodes[0]
            route.append(current_node)
        else:
            # Visit the node with the maximum prizes/distance ratio
            visited.add(max_ratio_node)
            prizes += max_ratio_node.capacity
            distance = dist_matrix[current_node.id - 1][max_ratio_node.id - 1]
            energy_consumption = distance * 0.002
            cost += distance
            energy_budget -= energy_consumption
            current_node = max_ratio_node
            route.append(current_node)

    # End timer
    # Return to node 0
    energy_consumption = dist_matrix[current_node.id - 1][0] * 0.002
    cost += dist_matrix[current_node.id - 1][0]
    energy_budget -= energy_consumption
    route.append(graph.nodes[0])
    end_time = time.time()

    # Print results
    print("\nRunning Greedy Algorithm 2 :")
    print("Route:", [node.id for node in route])
    print("Cost:", cost)
    print("Total prizes:", prizes)
    print("Energy budget Left:", initial_energy-energy_budget)
    print("Running time:", end_time - start_time)
    visualize_route(graph,route)

GreedyAlgorithm2(graph,initial_energy)
def MARL(graph, initial_energy):
    # Initialize the Q-values for each agent and action
    num_agents = 50
    max_steps = 200
    alpha = 0.9
    gamma = 0.9
    Q = {}
    total_distance=0
    prize=0
    dist_matrix = [[node.distance(other) for other in graph.nodes] for node in graph.nodes]
    
    for agent in range(num_agents):
        for node in graph.nodes:
            Q[(agent, node)] = {}
            for neighbor in graph.nodes:
                Q[(agent, node)][neighbor] = 0

    # Initialize the current state for each agent
    current_state = {}
    for agent in range(num_agents):
        current_state[agent] = (graph.nodes[0], initial_energy, {})

    # Initialize the total reward and number of steps
    total_reward = 0
    step = 0

    # Initialize the route and prizes
    route = [graph.nodes[0]]
    prizes = 0

    # Start the timer
    start_time = time.time()
    current_state = {}
    for agent in range(num_agents):
        current_state[agent] = (graph.nodes[0], initial_energy, {}, [])
    # Run the MARL algorithm for a maximum of max_steps
    while step < max_steps:
        # Initialize the rewards and next states for each agent
        rewards = {}
        next_states = {}
        
        # Take an action for each agent based on its current state and policy
        for agent in range(num_agents):
            state = current_state[agent]
            neighbors = [n for n in graph.nodes if n != state[0]]
            if len(state[2]) == len(graph.dns):  # if all DNs have been visited, return to the starting node
                action = graph.nodes[0]
                
            else:
                unvisited_dns = set(graph.dns) - set(state[2].keys())
                nearest_dn = min(unvisited_dns,
                                key=lambda dn: dn[1] - state[0].distance(graph.nodes[dn[0] - 1]))
                unvisited_nodes = [n for n in neighbors if n not in state[2]]
                
                # Filter out visited nodes from the unvisited nodes
                unvisited_nodes = [n for n in unvisited_nodes if n not in state[3]]

                
                if len(unvisited_nodes) > 0:
                    action = min(unvisited_nodes,
                                key=lambda node: dist_matrix[state[0].id - 1][node.id - 1])
                else:
                    action = graph.nodes[0]  # Return to the starting node if all neighbors have been visited
            
            # ...

            # Move to the next state based on the selected action
            distance = dist_matrix[state[0].id - 1][action.id - 1]
            distance_traveled = action.distance(state[0])
            energy_cost = action.distance(state[0]) * 0.002  # Calculate the energy cost based on the distance traveled
            next_energy = state[1] - energy_cost
            total_distance += distance
            next_state = (action, next_energy, state[2].copy(), state[3].copy())
            if action.id in [dn[0] for dn in graph.dns]:
                next_state[2][action.id] = 1


            # Add the action to the visited list
            next_state[3].append(action)

            # Check if there is enough energy to go back to the start node before going to the next node
            if len(next_state[2]) == len(graph.dns):
                energy_cost_to_start = action.distance(graph.nodes[0]) * 0.002
                if next_energy - energy_cost_to_start < 0:
                    next_state = (state[0], next_energy, state[2].copy())  # Stay in the current node

            # Compute the reward for the selected action
            unvisited_dns = set(graph.dns) - set(next_state[2].keys())
            reward = -min([dn[1] - action.distance(graph.nodes[dn[0]-1]) for dn in unvisited_dns]) - 0.1 * action.distance(state[0])

            # Save the rewards and next states for each agent
            rewards[agent] = reward
            next_states[agent] = next_state
            
    
        
        # Update the Q-values for each agent and action based on the rewards and next states
        for agent in range(num_agents):
            state = current_state[agent]
            action = next_states[agent][0]
            reward = rewards[agent]
            next_state = next_states[agent]

        # Update Q-value for the current state and action
        if (agent, state[0]) not in Q:
            Q[(agent, state[0])] = {}
        if action not in Q[(agent, state[0])]:
            Q[(agent, state[0])][action] = 0
        Q[(agent, state[0])][action] += alpha * (reward + gamma * max([Q[(agent, next_state[0])][n] for n in graph.nodes])            - Q[(agent, state[0])][action])

        # Update the current state for each agent
        for agent in range(num_agents):
            current_state[agent] = next_states[agent]

        # Update the total reward and number of steps
        total_reward += sum(rewards.values())
        step += 1
        prize+=action.capacity
        # Update the route and prizes
        route.append(next_states[0][0])
        prizes += sum(next_states[0][2].values())

        # Check if all DNs have been visited or the energy budget has been exhausted
        if len(next_states[0][2]) == len(graph.dns) or next_states[0][1] <= 0:
            break

    # Calculate the remaining energy budget
    remaining_energy = current_state[0][1]

    # Calculate the running time of the algorithm
    running_time = time.time() - start_time

    # Print the results
    route.append(graph.nodes[0])
    prize+=graph.nodes[0].capacity
    print("\nRunning Multi Agent Reinforcement Learning :")
    route_values = [node.id for node in route]
    print(route_values)
    total_distance = 0.0
    for i in range(len(route) - 1):
        current_node = route[i]
        next_node = route[i + 1]
        
        distance = dist_matrix[current_node.id - 1][next_node.id - 1]
        
        total_distance += distance
    remaining_energy=total_distance*0.002

    print("Cost of the route: ", total_distance)
    print("Total prizes along the route: ", prize)
    print("Left budget (battery power) of the robot: ", initial_energy-remaining_energy)
    print("Running time of the algorithm: ", running_time)
    visualize_route(graph,route)
    return route, initial_energy - remaining_energy, prizes, remaining_energy, running_time


MARL(graph,initial_energy)