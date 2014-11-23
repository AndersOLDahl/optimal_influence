#!/usr/bin/python

import sys
import heapq

# Employee
ID = 0
BOSS_ID = 1
VALUE = 2

# Node data
NODE_LEAF = 0
NODE_CHILDREN = 1
NODE_VALUE = 2

# Priority queue data
QUEUE_LEAF = 0
QUEUE_VALUE = 1

# Start point for the priority queue (id = 1)
CEO = 1

# Priority queue class using heapq which is a binary heap. This will make
# finding the maximum very fast.
class PriorityQueue:
  def __init__(self):
    self._queue = []
    self._index = 0

  def push(self, item, priority):
    heapq.heappush(self._queue, (-priority, self._index, item))
    self._index += 1

  def pop(self):
    return heapq.heappop(self._queue)[-1]

# Read data from the standard input. Assumes it comes in the right format.
def readSTDIN():
  N, k = map(int, sys.stdin.readline().split(" "))

  # Make ids match indexes
  employees = [[0,0,0]]
  for i in range(N):
    line = sys.stdin.readline()[:-1].split(" ")
    numbers = map(int, line)
    employees.append(numbers)
  return employees, k, N

# Find the leaf nodes from the data. These are the data points that never get
# mentioned as another node's BOSS_ID
def find_leaf_nodes(employees, N):
  find_leaf_nodes = [True] * (N + 1)
  leaf_nodes = []

  for employee in employees:
    if find_leaf_nodes[employee[BOSS_ID]] == True:
      find_leaf_nodes[employee[BOSS_ID]] = False

  for index, leaf in enumerate(find_leaf_nodes):
    if leaf == True:
      leaf_nodes.append(index)

  return leaf_nodes

# Initalize important data for each node
#   [0,[],0]
#   - The leaf node that leads to the highest accumulated value from
#   this node
#   - Direct children from the node
#   - Highest accumulated value from this node to a leaf node
def initalize_tree(employees, leaf_nodes, N):

  data = [[0, [], 0] for _ in range(N+1)]
  added_already = [False] * (N + 1)

  for leaf in leaf_nodes:
    next_node = employees[leaf][BOSS_ID]
    accumulated_value = employees[leaf][VALUE]
    data[leaf][NODE_LEAF] = leaf
    data[next_node][NODE_CHILDREN].append(leaf)
    data[leaf][NODE_VALUE] = accumulated_value

    # Loop until the CEO, it might short circut beforehand
    while(next_node != 0):
      current_node = next_node
      next_node = employees[current_node][BOSS_ID]

      # If we have already added this node once, we do not
      # need to add it again.
      if(added_already[current_node] != True):
        data[next_node][NODE_CHILDREN].append(current_node)
        added_already[current_node] = True

      accumulated_value += employees[current_node][VALUE]

      # Change the stored accumulated value if it is greater than what we had
      # before; otherwise, short circuit to avoid unnecessary looping
      if (accumulated_value > data[current_node][NODE_VALUE]):
        data[current_node][VALUE] = accumulated_value
        data[current_node][NODE_LEAF] = leaf
      else:
        break

  return data

# Find the maximum influence you can spread by picking k employees
def find_maximum_influence(data, employees, k, N):

  # Used to stop if a calculation reaches a deleted node at any point
  flag_deleted_nodes = [False] * (N + 1)
  current_maximum = 0

  # Push the CEO onto the priority queue
  priority_queue = PriorityQueue()
  priority_queue.push([data[CEO][NODE_LEAF], data[CEO][VALUE]], data[CEO][VALUE])

  # Loop through k amount of times
  for x in range (0, k):

    # Pop off the max
    temp = priority_queue.pop()
    current_node = temp[QUEUE_LEAF]
    current_maximum += temp[QUEUE_VALUE]

    # Mark the leaf we are working with as deleted
    flag_deleted_nodes[current_node] = True
    next_node = employees[current_node][BOSS_ID]

    # Loop until the CEO or a deleted node is reached
    while(next_node != 0 and flag_deleted_nodes[next_node] != True):
      current_node = next_node

      # Flag that we have deleted the node
      flag_deleted_nodes[current_node] = True
      next_node = employees[current_node][BOSS_ID]

      # Add the now seperate trees to the priority queue. Make sure they
      # have not been deleted before doing so.
      for e in data[current_node][NODE_CHILDREN]:
        if (flag_deleted_nodes[e] != True):
          priority_queue.push([data[e][NODE_LEAF], data[e][VALUE]], data[e][VALUE])

  # Return the maximum influence for k iterations
  return current_maximum

def Algorithm():

  # Read the employees and make the id's match indexes. This will be easier to
  # work with.
  employees, k, N = readSTDIN()

  # Keep track of all the leaf nodes in the tree
  leaf_nodes = find_leaf_nodes(employees, N)

  # Keep track of important computational data for all nodes
  data = initalize_tree(employees, leaf_nodes, N)

  print find_maximum_influence(data, employees, k, N)

if __name__ == "__main__":
  Algorithm()

