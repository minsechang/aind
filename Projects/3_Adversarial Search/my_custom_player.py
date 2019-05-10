from sample_players import DataPlayer
import random
# from isolation import _WIDTH, _HEIGHT, _SIZE
_WIDTH=11
_HEIGHT=9

from isolation import Isolation, DebugState
import math

def get_penalty_value(index, ply_count):
    """ Convert from board index value to xy coordinates

    The coordinate frame is 0 in the bottom right corner, with x increasing
    along the columns progressing towards the left, and y increasing along
    the rows progressing towards teh top.
    """
    x = index % (_WIDTH + 2)
    y = index // (_WIDTH + 2)
    penalty = 0

    if x == 0 or x == _WIDTH-1 or y == 0 or y == _HEIGHT-1:
        penalty = 2
    elif x == 1 or x == _WIDTH-2 or y == 1 or y == _HEIGHT-2:
        penalty = 1

    if ply_count > 70:
        penalty = penalty * 3
    elif ply_count > 40:
        penalty = penalty * 2

    return penalty

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        # For the first move, randomly pick a state which is closest from the center.
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
            # self.queue.put(self.initialize(state))
        for i in range(2,6):
            self.queue.put(self.alpha_beta_search(state, depth=i))

    # def initialize(self, state):
    #     def dist_from_center(index):
    #         x,y = DebugState.ind2xy(index)
    #         return math.sqrt((_WIDTH/2.0-x)**2+(_HEIGHT-y)**2)
    #     choices = []
    #     for i in range(INITIAL_RANDOM_PICKS):
    #         choices.append(random.choice(state.actions()))
    #     return min(choices, key=lambda x: dist_from_center(state.result(x).locs[self.player_id]))


    def alpha_beta_search(self, state, depth):

        def min_value(state, alpha, beta, depth):
            # check for terminating state
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.get_heuristic_score(state)
            value = float("inf")

            for action in state.actions():
                new_state = state.result(action)
                value = min(value, max_value(new_state, alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_value(state, alpha, beta, depth):
            # check for terminating state
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.get_heuristic_score(state)

            value = float("-inf")
            for action in state.actions():
                new_state = state.result(action)
                value = max(value, min_value(new_state, alpha, beta, depth - 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

        actions = state.actions()
        return max(actions, key=lambda x: min_value(state.result(x), float('-inf'), float('inf'), depth - 1))


    def get_heuristic_score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)

        #Penalize moves that make the knight to move to far corners
        penalty = get_penalty_value(own_loc, state.ply_count)
        # return len(own_liberties) - len(opp_liberties)
        return len(own_liberties) - len(opp_liberties) - penalty
