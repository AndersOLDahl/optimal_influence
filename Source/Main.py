#!/usr/bin/python

import sys
import heapq

ID = 0
BOSS_ID = 1
VALUE = 2

NODE_LEAF = 0
NODE_CHILDREN = 1

CEO = 1

class PriorityQueue:
  def __init__(self):
    self._queue = []
    self._index = 0

  def push(self, item, priority):
    heapq.heappush(self._queue, (-priority, self._index, item))
    self._index += 1

  def pop(self):
    return heapq.heappop(self._queue)[-1]

def readSTDIN():

  N, k = map(int, sys.stdin.readline().split(" "))
  employees = []
  for i in range(N):
    line = sys.stdin.readline()[:-1].split(" ")
    numbers = map(int, line)
    employees.append(numbers)
  return employees, k, N

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

def initalize_tree(employees, leaf_nodes, N):

  data = [[0, [], 0] for _ in range(N+1)]
  added_already = [False] * (N + 1)

  for leaf in leaf_nodes:
    next_node = employees[leaf][BOSS_ID]
    accumulated_value = employees[leaf][VALUE]
    data[leaf][NODE_LEAF] = leaf
    data[next_node][NODE_CHILDREN].append(leaf)
    data[leaf][VALUE] = accumulated_value

    while(next_node != 0):
      current_node = next_node
      next_node = employees[current_node][BOSS_ID]

      if(added_already[current_node] != True):
        data[next_node][NODE_CHILDREN].append(current_node)
        added_already[current_node] = True

      accumulated_value += employees[current_node][VALUE]
      if (accumulated_value > data[current_node][VALUE]):
        data[current_node][VALUE] = accumulated_value
        data[current_node][NODE_LEAF] = leaf
      else:
        break

  return data

def delete_path(priority_queue, data, employees, flag_deleted_nodes, current_maximum):

  temp = priority_queue.pop()
  current_node = temp[0]
  current_maximum += temp[1]
#  print temp[0]
#  print temp[1]
  flag_deleted_nodes[current_node] = True

  next_node = employees[current_node][BOSS_ID]
  while(next_node != 0 and flag_deleted_nodes[next_node] != True):
    current_node = next_node
    flag_deleted_nodes[current_node] = True
    next_node = employees[current_node][BOSS_ID]

    for e in data[current_node][NODE_CHILDREN]:
    #  print data[current_node][NODE_CHILDREN], e
      if (flag_deleted_nodes[e] != True):
    #    print "PUSHING TO Priority Queue", [e, data[e][VALUE]], "\n"
        priority_queue.push([data[e][NODE_LEAF], data[e][VALUE]], data[e][VALUE])

  return priority_queue, flag_deleted_nodes, current_maximum

def find_maximum_value(data, employees, k, N):

  flag_deleted_nodes = [False] * (N + 1)
  current_maximum = 0
  priority_queue = PriorityQueue()
  priority_queue.push([data[CEO][NODE_LEAF], data[CEO][VALUE]], data[CEO][VALUE])

  for x in range (0, k):
    priority_queue, flag_deleted_nodes, current_maximum = delete_path(priority_queue, data, employees, flag_deleted_nodes, current_maximum)

  return current_maximum

def Algorithm():

  # Read the employees and make the id's match indexes
  employees, k, N = readSTDIN()
  employees = [[0,0,0]] + employees

  # Keep track of all the leaf nodes in the tree
  leaf_nodes = find_leaf_nodes(employees, N)

  # Keep track of the data for all nodes
  data = initalize_tree(employees, leaf_nodes, N)

  maximum = find_maximum_value(data, employees, k, N)
  print maximum
  return maximum

if __name__ == "__main__":
  Algorithm()

