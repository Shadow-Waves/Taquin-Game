from Stack import Stack
from itertools import chain
from copy import deepcopy

class Taquin: 
    def __init__(self,matrix = [[1,2,3],[4,5,0],[6,7,8]],size = 3):
        self.size = size
        self.initial_configuration = matrix
        self.goal_configuration = [[*range(i,i + 3)] for i in range(1,size**2,3)]
        assert self.is_solvable() ,"NOT SOLVABLE"

    def is_solvable(self):
        main_matrix = list(chain(self.initial_configuration))
        inversion = len([(i,j) for i in main_matrix for j in main_matrix if i != j if i > j if main_matrix.index(i) < main_matrix.index(j) if not 0 in [i,j]])
        blank_pos_from_button = self.size - [i for i in range(self.size) for j in range(self.size) if self.initial_configuration[i][j] == 0][0]
        if self.size % 2 and inversion % 2 == 0:
            return True
        elif (self.size % 2 == 0) and ((blank_pos_from_button % 2 == 0 and inversion % 2) or (blank_pos_from_button % 2 and inversion % 2 == 0)):
            return True
        else:
            return False
                
    def is_valid_state(self,matrix,node):
        if node != 0:
            x0,y0 = [(i,j) for i in range(self.size) for j in range(self.size) if matrix[i][j] == 0][0]
            xnode,ynode = [(i,j) for i in range(self.size) for j in range(self.size) if matrix[i][j] == node][0]
            return True if abs(x0 - xnode) + abs(y0 - ynode) == 1 else False
    
    def action(self,matrix,node):
        if self.is_valid_state(matrix,node):
            copy = deepcopy(matrix)
            x0,y0 = [(i,j) for i in range(self.size) for j in range(self.size) if matrix[i][j] == 0][0]
            xnode,ynode = [(i,j) for i in range(self.size) for j in range(self.size) if matrix[i][j] == node][0]
            copy[x0][y0],copy[xnode][ynode] = copy[xnode][ynode],copy[x0][y0]
            return copy
        
    def successors_list(self,matrix):
        x0,y0 = [(i,j) for i in range(self.size) for j in range(self.size) if matrix[i][j] == 0][0]
        nearest_neighbors = [
            matrix[x0 - 1][y0] if x0 - 1 >= 0 else None,
            matrix[x0 + 1][y0] if x0 + 1 < self.size else None,
            matrix[x0][y0 - 1] if y0 - 1 >= 0 else None,
            matrix[x0][y0 + 1] if y0 + 1 < self.size else None,
        ]
        return [self.action(matrix,node) for node in nearest_neighbors if node]
    
    def A_star(self):
        g = 0
        open_list = [[self.initial_configuration,g,len([1 for i in range(self.size) for j in range(self.size) if self.initial_configuration[i][j] != self.goal_configuration[i][j]])]]
        closed_list = []
        while True:
            node = open_list.pop(0)
            closed_list.append(node)
            if node[2] == 0:
                paths.write(f"{self.initial_configuration} : {g} : {closed_list}\n")
                return g
            g += 1
            for item in self.successors_list(node[0]):
                x = len([1 for i in range(self.size) for j in range(self.size) if item[i][j] != self.goal_configuration[i][j] if item[i][j]])
                y = [i[0] for i in open_list] + [i[0] for i in closed_list]
                if not item in y:
                    open_list.append([item,g,x])
            open_list = sorted(open_list,key = lambda y:y[1] + y[2],reverse = False)
        

    def BFS(self):
        visited = [self.initial_configuration]
        queue = [self.initial_configuration]
        k = 0
        while queue:
            s = queue.pop(0)
            k += 1
            if s == self.goal_configuration:
                return k,visited
            for i in self.successors_list(s):
                if not i in visited:
                    queue.append(i)
                    visited.append(i)

    def DFS(self):
        stack = Stack(self.initial_configuration)
        path = []
        k = 0
        while not stack.is_empty():
            vertex = stack.pop()
            k += 1
            if vertex == self.goal_configuration:
                return k,path
            if vertex in path:
                continue
            path.insert(0,vertex)
            for neighbor in self.successors_list(vertex):
                stack.append(neighbor)
                
if __name__ == "__main__":
    taquin = Taquin([[1,2,3],[4,5,0],[7,8,6]],3)
    paths = open("paths.txt",'a')
    print(taquin.A_star())
    paths.close()