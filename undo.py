from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import *
from action import PaintAction

class UndoTracker:
    def __init__(self):
        """
        Initialising undoTracker and redoTracker as stacks as this ADT operates on a LIFO basis, so undoing an action (pop from
        first stack) and then pushing onto the second stack so that if redo is called, then pop action from second stack.

        INPUT: None
        RAISE: None
        OUTPUT: None

        Complexity: best = worst = O(1) since intialising is always constant
        """
        self.undoTracker = ArrayStack(100)
        self.redoTracker = ArrayStack(100)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.

        INPUTS: Action
        RAISE: None
        OUTPUTS: None

        Complexity: best = worst = O(1), since pushing onto a stack is always constant
        """
        self.undoTracker.push(action)

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.

        INPUTS: Grid
        RAISE: None
        OUTPUTS: None or PaintAction (action)

        Complexity: checking if the stack is empty is always O(1), and popping is also O(1), measured against the grid. However, if
        the Draw Style is sequential and special() is called, then the worst-case complexity is O(len(self.layerstore)).
        """
        if self.undoTracker.is_empty():
            return None
        else:
            action = self.undoTracker.pop()
            action.undo_apply(grid)
            return action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.

        INPUTS: Grid
        RAISE: None
        OUTPUTS: PaintAction (action) or None

        Complexity: checking if the stack is empty is always O(1), and popping is also O(1). However, if
        the Draw Style is sequential and special() is called, then the worst-case complexity is O(len(self.layerstore)).
        """
        if self.redoTracker.is_empty():
            return None
        else:
            action = self.redoTracker.pop()
            action.redo_apply(grid)
            return action
