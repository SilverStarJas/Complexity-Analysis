from __future__ import annotations
from action import PaintAction
from grid import Grid
from undo import *
from data_structures.queue_adt import CircularQueue

class ReplayTracker: # using circular queue to serve actions in the order that they happened in


    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.

        INPUTS: None
        RAISE: None
        OUTPUTS: None

        Complexity: best-case is O(1) if there is only one action to replay, best-case is O(len(self.replay_tracker)), if it has 
        to replay more than one action, thus serving each item in the tracker.
        """
        self.replay_tracker = CircularQueue(100)
        # use for loop to serve actions
        for i in range(len(self.replay_tracker)):
            self.replay_tracker.serve()
        
        

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.

        INPUT: Action (PaintAction), is_undo (boolean value)
        RAISE: None
        OUTPUT: None

        Complexity: best = worst = O(1), since appending an item to a queue is always constant
        """
        self.replay_tracker.append(action)

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        INPUTS: grid
        RAISE: None
        OUTPUTS: True (boolean value), grid (array) with the action applied on it
        """
        if self.replay_tracker.is_empty():
            return True
        else:
            self.replay_tracker.serve(grid)
            return grid

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

