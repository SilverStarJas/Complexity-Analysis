from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import *

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore): # only one layer so no ADTs used
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """
    def __init__(self) -> None:
        """
        INPUTS: None
        RAISE: None
        OUTPUTS: None

        Complexity: O(1), since it is initialising one layer
        """
        self.layer = None
        self.is_special = False # special() func. won't be called

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.

        INPUTS: layer
        RAISE: None
        OUTPUTS: Boolean value

        Complexity: best = worst = O(1) in this case because only one layer is added, and any new layers will override the previous
        layer store. These operations are always constant.
        """
        if self.layer != layer: 
            self.layer = layer # add layer if there isn't one
            return True
        else:
            return False 

    def get_color(self, start: tuple, timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        INPUTS: Starting color (tuple), timestamp (integer), x (integer), y(integer)
        RAISE: None
        OUTPUTS: Colour of the square (tuple)

        Complexity: best = worst = O(1) because the input will tell the function which square to check the colour of. 
        """        
        # Complexity: O()
        if self.layer == None:
            color = start
        else:
            color = self.layer.apply(start,timestamp,x,y) # get colour of layer input

        # after special is called and colour is inverted
        if self.is_special:
            color = (255-color[0],255-color[1],255-color[2])
        
        return color
    
    def erase(self,layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        Setting the layer to none will replace the previous value of the variable, which was layer. 

        INPUTS: layer
        RAISE: None
        OUTPUTS: Boolean value

        Complexity: best = worst = O(1), because there is only one layer to remove/only need to check once if there is a layer.
        The check and the removal of the layer are both constant.
        """
        if self.layer != None:
            self.layer = None # removes if there is an existing layer
            return True
        else:
            return False

    def special(self):
        """
        Special mode. Different for each store implementation.

        INPUTS: None
        RAISE: None
        OUTPUTS: None

        Complexity: best = worst = O(1), since inverting the colour only requires subtracting the integers in the tuple.
        """
        self.is_special = not self.is_special

class AdditiveLayerStore(LayerStore): # using CircularQueue ADTs for this class
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    def __init__(self) -> None:
        """   
        INPUTS:  None
        RAISE: None
        OUTPUTS: None

        Complexity: best = worst = O(1), each time a layer is initialised is constant
        """
        self.layerstore = CircularQueue(100)
        self.is_special = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store, which will place it in the Circular Queue.
        Returns true if the LayerStore was actually changed.

        INPUTS: Layer
        RAISE: None
        OUTPUTS: Boolean value

        Complexity: best = worst = O(1), since checking if the queue is full and appending to a queue is always constant.
        """
        if self.layerstore.is_full:
            return("Maximum layers reached.")
        else:
            self.layerstore.append(layer)
            return True

    def get_color(self, start: tuple, timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers. If the layer isn't empty, the top layer is served
        and we get the colour of the layer. We then append it back to the Circular Queue so that the layer is not deleted.

        INPUTS: Starting color (tuple), timestamp (integer), x (integer), y(integer)
        RAISE: None
        OUTPUTS: color (tuple)

        Complexity: best-case is O(1), if the square is the first in the queue, worst-case is O(len(self.layerstore)) if it has to
        run through each layer.
        """        
        if self.layerstore.is_empty():
            color = start

        else: 
            color = start
            for i in range(len(self.layerstore)): # each item is a LayerStore of the layer
                layer = self.layerstore.serve()
                color = layer.apply(start,timestamp,x,y) # get colour of layer input
                self.layerstore.append(layer) # returning the layer to queue after serving
        
        return color

    
    def erase(self,layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.

        INPUTS: Layer
        RAISE: None
        OUTPUTS: Boolean value

        Complexity: best = worst = O(1), since checking if the queue is empty and serving from a queue is always constant.
        """
        if self.layerstore.is_empty():
            return("No layers to erase")
        else:
            self.layerstore.serve(layer)
            return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        For Additive, the layers will be reversed order.

        INPUTS: None
        RAISE: None
        OUTPUTS: None

        Complexity: The best-case complexity is O(1) if there is already a layer in the temporary stack which can be served. 
        The worst-case complexity is O(len(store)) if there are no elements in the temporary stack and we have to keep pushing and
        appending elements from the original layerstore.
        """
        stack = ArrayStack(self.layerstore.length)
        new_store = CircularQueue(self.layerstore.length)

        for i in range(self.layerstore.length):
            stack.push(self.layerstore.serve()) # pushes oldest layer to a temporary stack
        
        while not stack.is_empty():
            new_store.append(stack.pop()) # pop newest layer
        
        self.layerstore = new_store # new layer added


class SequenceLayerStore(LayerStore):  # couldn't figure out how to use BVset, used array sorted list instead
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
        """
        Initialising the array sorted list for the layers to be stored in.

        INPUTS: None
        RAISE: None
        OUTPUTS: None

        Complexity: O(1), since initialising is constant.
        """
        self.layerstore = ArraySortedList(20)

    def add(self, layer: Layer) -> bool:
        """
        add: Ensure this layer type is applied. The new layer will be added into the list but it is not sorted.
        
        INPUTS: Layer
        RAISE: None
        OUTPUTS: Boolean value

        Complexity: best = worst = O(1), since the layers are added but not sorted, so it will always be constant and add the
        layer to the end of the list.
        """
        item = layer.index
        tempitem = ListItem(layer,item)
        self.layerstore.add(tempitem)
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers. For each layer, it will check the colour of the 
        grid square at (x,y)
        
        INPUTS: Starting color (tuple), timestamp (integer), x (integer), y(integer)
        RAISE: None
        OUTPUTS: color (tuple)

        Complexity: best-case is O(1), if the square is in the first layer, so it is first in the list. The worst-case is 
        O(len(self.layerstore)) if it has to run through the entire list.
        """   
        if self.layerstore.is_empty():
            color = start
        else:
            color = start # initial layer
            for i in range(len(self.layerstore)):
                layer = self.layerstore.__getitem__(i)
                color = layer.value.apply(start, timestamp, x, y)
        
        return color
                           

    def erase(self,layer: Layer) -> bool:
        """
        erase: Ensure this layer type is not applied. The for loop will run through every layer and if the index matches the item,
        then the value at that index will be deleted.

        INPUTS: Layer
        RAISE: None
        OUTPUTS: Boolean value (True if erased)

        Complexity: best-case is O(1), if there is only one layer. The worst-case is O(len(self.layerstore)) if it has to 
        run through the entire list.
        """
        for i in range(len(self.layerstore)):
            item = self.layerstore.__getitem__(i)
            if item.value.name == layer.name:
                self.layerstore.delete_at_index(i)
                return True

    def special(self):
        """
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
        """
        # item = self.layer.name
        pass