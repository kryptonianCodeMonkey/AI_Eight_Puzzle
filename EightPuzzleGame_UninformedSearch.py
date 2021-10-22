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
        # check if state s is in openlist, if so return 2
        for state in self.openlist:
            if s.equals(state):
                return 2
        # Check if state s is in closed, if so return 3
        for state in self.closed:
            if s.equals(state):
                return 3

        # state s was in neither list, return 1
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
        # initialize tmp_array to be an array of 0's with dimensions matching walk_state
        tmp_arr = [[0 for x in range(walk_state.shape[0])] for y in range(walk_state.shape[1])]

        ### ↑(move up) action ###
        # (row - 1) is checked to prevent out of bounds errors, the tile is swapped with the one above it
        if (row - 1) >= 0:
            # copy walk_state to tmp_arr
            for i in range(walk_state.shape[0]):
                for j in range(walk_state.shape[1]):
                    tmp_arr[i][j] = walk_state[i][j]
            # swap 0 tile in tmp_arr with tile above it
            tmp_arr[row][col] = tmp_arr[row - 1][col]
            tmp_arr[row - 1][col] = 0
            # create new state object with tmp_array state, current depth, and no weight
            tmp_state = State(np.array([[tmp_arr[0][0], tmp_arr[0][1], tmp_arr[0][2]],
                                         [tmp_arr[1][0], tmp_arr[1][1], tmp_arr[1][2]],
                                         [tmp_arr[2][0], tmp_arr[2][1], tmp_arr[2][2]]]), self.current.depth+1, 0)
            # determine if tmp_state already in open or closed lists
            flag = self.check_inclusive(tmp_state)
            # if tmp_state not in open or closed list, add to end of openlist
            if flag == 1:
                self.openlist.append(tmp_state)


        ### ↓(move down) action ###
        # (row + 1) is checked to prevent out of bounds errors, the tile is swapped with the one below it
        if (row + 1) < walk_state.shape[0]:
            # copy walk_state to tmp_arr
            for i in range(walk_state.shape[0]):
                for j in range(walk_state.shape[1]):
                    tmp_arr[i][j] = walk_state[i][j]
            # swap 0 tile in tmp_arr with tile below it
            tmp_arr[row][col] = tmp_arr[row + 1][col]
            tmp_arr[row + 1][col] = 0
            # create new state object with tmp_array state, current depth, and no weight
            tmp_state = State(np.array([[tmp_arr[0][0], tmp_arr[0][1], tmp_arr[0][2]],
                                         [tmp_arr[1][0], tmp_arr[1][1], tmp_arr[1][2]],
                                         [tmp_arr[2][0], tmp_arr[2][1], tmp_arr[2][2]]]), self.current.depth+1, 0)
            # determine if tmp_state already in open or closed lists
            flag = self.check_inclusive(tmp_state)
            # if tmp_state not in open or closed list, add to end of openlist
            if flag == 1:
                self.openlist.append(tmp_state)


        ### ←(move left) action ###
        # (col - 1) is checked to prevent out of bounds errors, the tile is swapped with the one to the left of it
        if (col - 1) >= 0:
            # copy walk_state to tmp_arr
            for i in range(walk_state.shape[0]):
                for j in range(walk_state.shape[1]):
                    tmp_arr[i][j] = walk_state[i][j]
            # swap 0 tile in tmp_arr with tile to left of it
            tmp_arr[row][col] = tmp_arr[row][col - 1]
            tmp_arr[row][col - 1] = 0
            # create new state object with tmp_array state, current depth, and no weight
            tmp_state = State(np.array([[tmp_arr[0][0], tmp_arr[0][1], tmp_arr[0][2]],
                                         [tmp_arr[1][0], tmp_arr[1][1], tmp_arr[1][2]],
                                         [tmp_arr[2][0], tmp_arr[2][1], tmp_arr[2][2]]]), self.current.depth+1, 0)
            #  determine if tmp_state already in open or closed lists
            flag = self.check_inclusive(tmp_state)
            # if tmp_state not in open or closed list, add to end of openlist
            if flag == 1:
                self.openlist.append(tmp_state)


        ### →(move right) action ###
        # (col + 1) is checked to prevent out of bounds errors, the tile is swapped with the one tot he right of it
        if (col + 1) < walk_state.shape[1]:
            # copy walk_state to tmp_arr
            for i in range(walk_state.shape[0]):
                for j in range(walk_state.shape[1]):
                    tmp_arr[i][j] = walk_state[i][j]
            # swap 0 tile in tmp_arr with tile to right of it
            tmp_arr[row][col] = tmp_arr[row][col + 1]
            tmp_arr[row][col + 1] = 0
            # create new state object with tmp_array state, current depth, and no weight
            tmp_state = State(np.array([[tmp_arr[0][0], tmp_arr[0][1], tmp_arr[0][2]],
                                         [tmp_arr[1][0], tmp_arr[1][1], tmp_arr[1][2]],
                                         [tmp_arr[2][0], tmp_arr[2][1], tmp_arr[2][2]]]), self.current.depth+1, 0)
            # determine if tmp_state already in open or closed lists
            flag = self.check_inclusive(tmp_state)
            # if tmp_state not in open or closed list, add to end of openlist
            if flag == 1:
                self.openlist.append(tmp_state)

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

