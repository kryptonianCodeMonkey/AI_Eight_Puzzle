import numpy as np
from EightPuzzleGame_State import State

'''
This class implement one of the Uninformed Search algorithm
You may choose to implement the Breadth-first or Depth-first or Iterative-Deepening search algorithm

'''


class UninformedSearchSolver:
    current = State()
    goal = State()
    openlist = []
    closed = []
    depth = 0

    def __init__(self, current, goal):
        self.current = current
        self.goal = goal
        self.openlist.append(current)


    def check_inclusive(self, s):
        """
        * The check_inclusive function is designed to check if the expanded state is or is not in open list or closed list
        * This is done to prevent looping
        * @param s
        * @return
        """

        #TODO your code start here
        #Check if state s is in openlist, if so return 2
        for state in self.openlist:
            if s.equals(state):
                return 2
        #Check if state s is in closed, if so return 3
        for state in self.closed:
            if s.equals(state):
                return 3

        #state s was in neither list, return 1
        return 1

        #TODO your code end here



    def state_walk(self):
        """
        * The following state_walk function is designed to move the blank tile --> perform actions
         * There are four types of possible actions/walks of for the blank tile, i.e.,
         *  ↑ ↓ ← → (move up, move down, move left, move right)
         * Note that in this framework the blank tile is represent by '0'
        """

        # First you need to remove the current node from the open array and move it to the closed array
        self.closed.append(self.current)
        self.openlist.remove(self.current)
        walk_state = self.current.tile_seq
        row = 0
        col = 0

        # Loop to find the location of the blank space
        for i in range(len(walk_state)):
            for j in range(len(walk_state[i])):
                if walk_state[i, j] == 0:
                    row = i
                    col = j
                    break

        self.depth += 1


        ''' The following program is used to do the state space actions
            The 4 conditions for moving the tiles all use similar logic, they only differ in the location of the 
            tile that needs to be swapped. That being the case, I will only comment the first subroutine
        '''
        # TODO your code start here
        ### ↑(move up) action ###
        #(row - 1) is checked to prevent out of bounds errors, the tile is swapped with the one above it
        if (row - 1) >= 0:
            array1d = self.current.getTile_1d()
            array1d[3*row+col] = array1d[3*(row-1)+col]
            array1d[3*(row-1)+col] = 0
            temp_state = State(np.array([[array1d[0], array1d[1], array1d[2]], [array1d[3], array1d[4], array1d[5]],
                                         [array1d[6], array1d[7], array1d[8]]]), self.current.depth+1, 0)
            flag = self.check_inclusive(temp_state)
            if flag == 1:
                self.openlist.append(temp_state)


        ### ↓(move down) action ###
        if (row + 1) <= 2:
            array1d = self.current.getTile_1d()
            array1d[3 * row + col] = array1d[3 * (row + 1) + col]
            array1d[3 * (row + 1) + col] = 0
            temp_state = State(np.array([[array1d[0], array1d[1], array1d[2]], [array1d[3], array1d[4], array1d[5]],
                                         [array1d[6], array1d[7], array1d[8]]]), self.current.depth+1, 0)
            flag = self.check_inclusive(temp_state)
            if flag == 1:
                self.openlist.append(temp_state)


        ### ←(move left) action ###
        if (col - 1) >= 0:
            array1d = self.current.getTile_1d()
            array1d[3 * row + col] = array1d[3 * row + col - 1]
            array1d[3 * row + col - 1] = 0
            temp_state = State(np.array([[array1d[0], array1d[1], array1d[2]], [array1d[3], array1d[4], array1d[5]],
                                         [array1d[6], array1d[7], array1d[8]]]), self.current.depth+1, 0)
            flag = self.check_inclusive(temp_state)
            if flag == 1:
                self.openlist.append(temp_state)


        ### →(move right) action ###
        if (col + 1) <= 2:
            array1d = self.current.getTile_1d()
            array1d[3 * row + col] = array1d[3 * row + col + 1]
            array1d[3 * row + col + 1] = 0
            temp_state = State(np.array([[array1d[0], array1d[1], array1d[2]], [array1d[3], array1d[4], array1d[5]],
                                         [array1d[6], array1d[7], array1d[8]]]), self.current.depth+1, 0)
            flag = self.check_inclusive(temp_state)
            if flag == 1:
                self.openlist.append(temp_state)

        # Set the next current state
        self.current = self.openlist[0]

        #TODO your code end here


    # # You can change the following code to print all the states on the search path
    def run(self):
        # output the goal state
        target = self.goal.tile_seq
        print("\nReached goal state: ")
        target_str = np.array2string(target, precision=2, separator=' ')
        print(target_str[1:-1])

        print("\n The visited states are: ")
        path = 0
        while not self.current.equals(self.goal):
            self.state_walk()
            print('Visited State number ', path+1)
            pathstate_str = np.array2string(self.current.tile_seq, precision=2, separator=' ')
            print(pathstate_str[1:-1])
            path += 1
        print("\n It took ", path, " iterations to reach to the goal state")
        print("The length of the path is: ", self.current.depth)

