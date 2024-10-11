from __future__ import annotations
from layer_store import *
from data_structures.referential_array import ArrayR


class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.

        INPUTS: draw_style (class), x (integer), y(integer)
        RAISE: None
        OUTPUTS: None

        Complexity: All assignments are constant, so the complexity is O(1)
        """

        self.draw_style = draw_style
        self.x = x
        self.y = y
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE

        """
        The grid is created as an array of arrays. Since each square is a layer store, it will add a square down y, which will
        create column. Then the columns are added into the array, creating rows x columns.
        
        The worst-case complexity of creating the grid is O(m*n), where m is the integer size of x and n is the integer size of y.
        The best-case complexity is O(1) if there is only one grid square. However, this would not be practical. 
        """
        self.grid = ArrayR(x)

        for i in range(len(self.grid)):
            yList = ArrayR(y)
            for j in range(len(yList)):
                yList[j] = SetLayerStore()
            self.grid[i] = yList

    # Complexity: O(1), since return is always constant time
    def __getitem__(self, index) -> LayerStore:
        return self.grid[index] 
        
    # Complexity: O(1), since all the operations are constant   
    def increase_brush_size(self) -> int:
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.

        INPUTS: None
        RAISE: None
        OUTPUTS: Integer

        Complexity: The comparison to check if the brush size is already max. and increasing the size are both constant operations, 
        so best = worst = O(1)
        """
        current_brush_size = self.brush_size
        size_increment = 1
        if current_brush_size >= Grid.MAX_BRUSH:
            print(f"Maximum brush size reached: {Grid.MAX_BRUSH}")
        else:
            current_brush_size += size_increment
            print(f"Brush size: {current_brush_size}")
        
    # Complexity: O(1), since all the operations are constant 
    def decrease_brush_size(self) -> int:
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.

        INPUTS: None
        RAISE: None
        OUTPUTS: Integer

        Complexity: The comparison to check if the brush size is already min. and decreaing the size are both constant operations, 
        so best = worst = O(1)
        """
        current_brush_size = self.brush_size
        size_increment = 1
        if current_brush_size <= Grid.MIN_BRUSH:
            print(f"Minimum brush size reached: {Grid.MIN_BRUSH}")
        else:
            current_brush_size -= size_increment
            print(f"Brush size: {current_brush_size}")
        

    def special(self):
        """
        Activate the special affect on all grid squares.

        INPUTS: None
        RAISE: None
        OUTPUTS: None

        Complexity: Depends on the draw style, please refer to layer_store.py DocStrings :)
        """
        DRAW_STYLE_SET = SetLayerStore
        DRAW_STYLE_ADD = AdditiveLayerStore
        DRAW_STYLE_SEQUENCE = SequenceLayerStore
        
        if self.DRAW_STYLE_OPTIONS == DRAW_STYLE_SET:
            SetLayerStore.special()
        if self.DRAW_STYLE_OPTIONS == DRAW_STYLE_ADD:
            AdditiveLayerStore.special()
        if self.DRAW_STYLE_OPTIONS == DRAW_STYLE_SEQUENCE:
            SequenceLayerStore.special()