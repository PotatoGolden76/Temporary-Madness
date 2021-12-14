class UndoService:

    def __init__(self):
        self._history = []
        self._index = -1
    # TODO: solve bug where if you undo, then do a new operation, the old redo queue won't get overwritten

    def record(self, operation):
        while len(self._history)-1 != self._index:
            self._history.pop()
        self._history.append(operation)
        self._index = len(self._history) - 1

    def undo(self):
        if self._index == - 1:
            print("No undos available")
        else:
            self._history[self._index].undo()
            self._index -= 1

    def redo(self):
        if self._index == len(self._history) - 1:
            print("No redos available")
        else:
            self._history[self._index].redo()
            self._index += 1


class Call:

    def __init__(self, function_name, *function_params):
        self._function_name = function_name
        self._function_params = function_params

    def call(self):
        self._function_name(*self._function_params)


class Operation:

    def __init__(self, undo_call, redo_call):
        self._undo_call = undo_call
        self._redo_call = redo_call

    def undo(self):
        self._undo_call.call()

    def redo(self):
        self._redo_call.call()


class CascadedOperation:

    def __init__(self):
        self._operations = []

    def add(self, operation):
        self._operations.append(operation)

    def undo(self):
        for op in self._operations:
            op.undo()

    def redo(self):
        for op in self._operations:
            op.redo()
