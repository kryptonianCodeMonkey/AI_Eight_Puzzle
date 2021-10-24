import numpy as np
from EightPuzzleGame_State import State
'''
This class implement the Best-First-Search (BFS) algorithm along with the Heuristic search strategies

In this algorithm, an Open list is used to store the unexplored states and 
a Closed list is used to store the visited state. Open list is a priority queue (First-In-First-Out). 
The priority is insured through sorting the Open list each time after new states are generated 
and added into the list. The heuristics are used to decide which node should be visited next.

In this informed search, reducing the state space search complexity is the main criterion. 
We define heuristic evaluations to reduce the states that need to be checked every iteration. 
Evaluation function is used to express the quality of informedness of a heuristic algorithm. 

'''

class InformedSearchSolver:
    current = State()
    goal = State()
    tf_goal = [] #transformed goal tile sequence used for heuristic 4
    openlist = []
    closed = []
    depth = 0

    def __init__(self, current, goal):
        self.current = current
        self.goal = goal
        self.openlist.append(current)
        #tf_goal is a transformation of the gaol sequence with horizontal and veritical swapped (mirrored over the diagonal)
        for y in range(goal.tile_seq.shape[1]):
            self.tf_goal.append([x for x in range(goal.tile_seq.shape[0])])
        for i in range(goal.tile_seq.shape[0]):
            for j in range(goal.tile_seq.shape[1]):
                self.tf_goal[j][i] = goal.tile_seq[i][j]

    def sortFun(self, e):
        return e.weight


    def check_inclusive(self, s):
        """
         * The check_inclusive function is designed to check if the expanded state is in open list or closed list
         * This is done to prevent looping. (You can use a similar code from uninformedsearch program)
         * @param s
         * @return
        """
        in_open = 0
        in_closed = 0
        ret = [-1, -1]

        # TODO your code start here
        # Check if state s is in openlist, if so ret[0] = 2 and ret[1] = state.depth
        for state in self.openlist:
            if s.equals(state):
                in_open = 1
                ret[0] = 2
                ret[1] = state.depth
        # Check if state s is in closed, if so ret[0] = 3 and ret[1] = state.depth
        for state in self.closed:
            if s.equals(state):
                in_closed = 1
                ret[0] = 3
                ret[1] = state.depth
        # state s was in neither list, ret[0] = 1
        if in_open == 0 & in_closed == 0:
            ret[0] = 1

        # return code and depth array, ret[]
        return ret
        # TODO your code start here


    def state_walk(self):
        """
        * The following state_walk function is designed to move the blank tile --> perform actions
        * There are four types of possible actions/walks of for the blank tile, i.e.,
        *  ↑ ↓ ← → (move up, move down, move left, move right)
        * Note that in this framework the blank tile is represent by '0'
        """
        # add closed state
        self.closed.append(self.current)
        self.openlist.remove(self.current)
        # move to the next heuristic state
        walk_state = self.current.tile_seq
        row = 0
        col = 0

        for i in range(len(walk_state)):
            for j in range(len(walk_state[i])):
                if walk_state[i, j] == 0:
                    row = i
                    col = j
                    break

        self.depth = self.current.depth + 1

        ''' The following program is used to do the state space actions
         The 4 conditions for moving the tiles all use similar logic, they only differ in the location of the 
         tile that needs to be swapped. That being the case, I will only comment the first subroutine'''
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
                                         [tmp_arr[2][0], tmp_arr[2][1], tmp_arr[2][2]]]), self.current.depth + 1, 0)
            # determine get list and depth of any states matching tmp_state already in openlist or closed list
            flag_depth = self.check_inclusive(tmp_state)
            # if tmp_state is in neither list, get heuristic weight and add to openlist
            if flag_depth[0] == 1:
                self.heuristic_test(tmp_state)
                self.openlist.append(tmp_state)
            # if tmp_state already in either list but depth is lower than state in list, remove it,
            # get heuristic weight of tmp_array and add tmp_state to openlist
            elif (flag_depth[0] == 2 | flag_depth[0] == 3) & flag_depth[1] > tmp_state.depth:
                list = self.openlist if flag_depth[0] == 2 else self.closed
                list.remove(tmp_state)
                self.heuristic_test(tmp_state)
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
                                        [tmp_arr[2][0], tmp_arr[2][1], tmp_arr[2][2]]]), self.current.depth + 1, 0)
            # determine get list and depth of any states matching tmp_state already in openlist or closed list
            flag_depth = self.check_inclusive(tmp_state)
            # if tmp_state is in neither list, get heuristic weight and add to openlist
            if flag_depth[0] == 1:
                self.heuristic_test(tmp_state)
                self.openlist.append(tmp_state)
            # if tmp_state already in either list but depth is lower than state in list, remove it,
            # get heuristic weight of tmp_array and add tmp_state to openlist
            elif (flag_depth[0] == 2 | flag_depth[0] == 3) & flag_depth[1] > tmp_state.depth:
                list = self.openlist if flag_depth[0] == 2 else self.closed
                list.remove(tmp_state)
                self.heuristic_test(tmp_state)
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
                                        [tmp_arr[2][0], tmp_arr[2][1], tmp_arr[2][2]]]), self.current.depth + 1, 0)
            # determine get list and depth of any states matching tmp_state already in openlist or closed list
            flag_depth = self.check_inclusive(tmp_state)
            # if tmp_state is in neither list, get heuristic weight and add to openlist
            if flag_depth[0] == 1:
                self.heuristic_test(tmp_state)
                self.openlist.append(tmp_state)
            # if tmp_state already in either list but depth is lower than state in list, remove it,
            # get heuristic weight of tmp_array and add tmp_state to openlist
            elif (flag_depth[0] == 2 | flag_depth[0] == 3) & flag_depth[1] > tmp_state.depth:
                list = self.openlist if flag_depth[0] == 2 else self.closed
                list.remove(tmp_state)
                self.heuristic_test(tmp_state)
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
                                        [tmp_arr[2][0], tmp_arr[2][1], tmp_arr[2][2]]]), self.current.depth + 1, 0)
            # determine get list and depth of any states matching tmp_state already in openlist or closed list
            flag_depth = self.check_inclusive(tmp_state)
            # if tmp_state is in neither list, get heuristic weight and add to openlist
            if flag_depth[0] == 1:
                self.heuristic_test(tmp_state)
                self.openlist.append(tmp_state)
            # if tmp_state already in either list but depth is lower than state in list, remove it,
            # get heuristic weight of tmp_array and add tmp_state to openlist
            elif (flag_depth[0] == 2 | flag_depth[0] == 3) & flag_depth[1] > tmp_state.depth:
                list = self.openlist if flag_depth[0] == 2 else self.closed
                list.remove(tmp_state)
                self.heuristic_test(tmp_state)
                self.openlist.append(tmp_state)

        # find the state in openlist with the best (lowest cost) evaluation of depth + weight
        lowest_cost = self.openlist[0].depth + self.openlist[0].weight
        best_state = self.openlist[0]
        for state in self.openlist:
            if state.depth + state.weight < lowest_cost:
                lowest_cost = state.depth + state.weight
                best_state = state
        # set current state to the one with the lowest cost
        self.current = best_state

        #TODO your code end here




    def heuristic_test(self, current):
        """
        * Solve the game using heuristic search strategies

        * There are three types of heuristic rules:
        * (1) Tiles out of place
        * (2) Sum of distances out of place
        * (3) 2 x the number of direct tile reversals

        * evaluation function
        * f(n) = g(n) + h(n)
        * g(n) = depth of path length to start state
        * h(n) = (1) + (2) + (3)
        """

        curr_seq = current.tile_seq
        goal_seq = self.goal.tile_seq

        # (1) Tiles out of place
        h1 = 0
        #TODO your code start here
        # count how many tiles are not in their corresponding goal location
        # loop over both current and goal states
        for (curr_row, goal_row) in zip(curr_seq, goal_seq):
            for (item1, item2) in zip(curr_row, goal_row):
                # if corresponding tiles don't match between current and goal states, increment h1
                if item1 != item2:
                    h1 += 1
        #TODO your code end here
        

        # (2) Sum of distances out of place
        h2 = 0
        #TODO your code start here
        # sum the distances that each tile is from its corresponding goal locations
        i_curr = 0
        j_curr = 0
        # loop over each tile in current state
        for curr_row in curr_seq:
            for item1 in curr_row:
                i_goal = 0
                j_goal = 0
                # loop over each tile in goal state to find corresponding tile
                for goal_row in goal_seq:
                    for item2 in goal_row:
                        if item1 == item2:
                            # match found, add vertical offset and horizontal offset to h2
                            h2 += abs(i_curr - i_goal) + abs(j_curr - j_goal)
                        j_goal += 1
                    i_goal += 1
                j_curr += 1
            i_curr += 1
        #TODO your code end here
        
        
        # (3) 2 x the number of direct tile reversals
        h3 = 0
        #TODO your code start here
        # check for any adjacent tiles that are mirrored from their goal state counterparts (costly to fix)
        # loop through each tile in both current and goal states
        for i in range(goal_seq.shape[0]):
            for j in range(goal_seq.shape[1]):
                # if tile is not at far right column, check the tile with the one to the right to see if it's mirrored,
                # if so, increment h3
                if i < goal_seq.shape[0] - 1 & goal_seq[i][j] == curr_seq[i+1][j] & goal_seq[i+1][j] == curr_seq[i][j]:
                    h3 +=1
                # if tile is not at bottom row, check the tile with the one below to see if it's mirrored,
                # if so, increment h3
                if j < goal_seq.shape[1] - 1 & goal_seq[i][j] == curr_seq[i][j+1] & goal_seq[i][j+1] == curr_seq[i][j]:
                    h3 +=1
        # double h3 because tile reversals are particularly hard to fix
        h3 *= 2

        # (Bonus) (4) total tiles out of row plus total tiles out of column
        # set h4 initial value to be the total titles in puzzle, then subtracting those in correct rows/columns
        h4 = goal_seq.shape[0] * goal_seq.shape[1]
        self.tf_goal
        #deduct number of current tiles in correct goal row
        for i in range(goal_seq.shape[0]):
            for j in range(goal_seq.shape[1]):
                if np.isin(curr_seq[i][j], goal_seq[i]):
                    h4 -= 1
        #deduct number of current tiles in correct goal column
        for j in range(goal_seq.shape[1]):
            for i in range(goal_seq.shape[0]):
                if np.isin(curr_seq[i][j], self.tf_goal[j]):
                    h4 -= 1

        # update the heuristic value for current state
        current.weight = h1 + h2 + h3 + h4

        #TODO your code end here

    # You can change the following code to print all the states on the search path
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
            print('Visited State number ', path + 1)
            pathstate_str = np.array2string(self.current.tile_seq, precision=2, separator=' ')
            print(pathstate_str[1:-1])
            path += 1

        print("\nIt took ", path, " iterations to reach to the goal state")
        print("The length of the path is: ", self.current.depth)

