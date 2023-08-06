from collections.abc import MutableSequence
from functools import singledispatch, update_wrapper, reduce
from types import LambdaType
from inspect import getsource

def method_dispatch(func):
    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper

def handle_inputs(conditional_statement=True):
    def decorator(func):
        def wrapper(self, expression=None, *args, **kwargs):
            # Return empty list if empty
            if len(self._list) == 0:
                return self.__class__()
            funcname = "List.{}".format(func.__name__)
            expressionType = type(expression)
            # Get type and check that it's proper.
            if conditional_statement:
                if expressionType == str:
                    if not any(operator for operator in self.operators if operator in expression):
                        raise TypeError("{}('expression') requires a conditional expression.".format(funcname))
                elif expressionType == LambdaType:
                    if not any(operator for operator in self.operators if operator in getsource(expression).split(":")[1]):
                        raise TypeError("{}('expression') requires a conditional expression.".format(funcname))
            # Convert str to lambda expression, else raise error.
            if expressionType == str:
                expression = eval("lambda x: {}".format(expression))
            elif expressionType == type(None):
                expression = eval("lambda x : x")
            elif expressionType != LambdaType:
                raise NotImplementedError("Unsupported type: {}. {}('expression') requires {} or {}.".format(expressionType, funcname, str, LambdaType))
            return func(self, expression, *args, **kwargs)
        return wrapper
    return decorator

class List(MutableSequence):
    operators = ["==","!=","<",">", "<=",">="]
    def __init__(self, data=None):
        super().__init__()
        if (data is not None):
            self._list = list(data)
        else:
            self._list = list()

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._list)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, ii):
        return self._list[ii]

    def __delitem__(self, ii):
        del self._list[ii]

    def __setitem__(self, ii, val):
        self._list[ii] = val

    def __str__(self):
        return str(self._list)

    def insert(self, ii, val):
        self._list.insert(ii, val)

    def append(self, val):
        self.insert(len(self._list), val)

    def element_error(self, item, message):
        print("Element '{}' produced the following {}: {}".format(item, message.__class__.__name__, message))

    @handle_inputs(conditional_statement=True)
    def where(self, expression):
        print("where running")
        newlist = []
        for item in self._list:
            try:
                if expression(item):
                    newlist.append(item)
            except Exception as message:
                self.element_error(item, message)
        return(self.__class__(newlist))

    @handle_inputs(conditional_statement=False)
    def select(self, expression):
        newlist = []
        for item in self._list:
            try:
                newlist.append(expression(item))
            except Exception as message:
                newlist.append(item)
                self.element_error(item, message)
        return(self.__class__(newlist))

    @handle_inputs(conditional_statement=True)
    def takewhile(self, expression):
        newlist = []
        for item in self._list:
            try:
                if expression(item):
                    newlist.append(item)
                else:
                    break
            except Exception as message:
                self.element_error(item, message)
                break
        return(self.__class__(newlist))

    @handle_inputs(conditional_statement=False)
    def groupby(self, expression):
        newdict = {}
        for item in self._list:
            try:
                expression_key = expression(item)
                if not (expression_key in newdict):
                    newdict[expression_key] = [item]
                else:
                    newdict[expression_key].append(item)
            except Exception as message:
                self.element_error(item, message)

        newlist = [{k:v} for k,v in newdict.items()]
        return(self.__class__(newlist))

    @handle_inputs(conditional_statement=False)
    def orderby(self, expression=None, reverse=False):
        newlist = self._list.copy()
        newlist.sort(key=expression, reverse=reverse)
        return(self.__class__(newlist))

    @handle_inputs(conditional_statement=True)
    def all(self, expression):
        newresult = True
        for item in self._list:
            try:
                if not expression(item):
                    newresult = False
                    break
            except Exception as message:
                self.element_error(item, message)
                newresult = False
                break

        return(newresult)

    @handle_inputs(conditional_statement=True)
    def any(self, expression):
        newresult = False
        for item in self._list:
            try:
                if expression(item):
                    newresult = True
                    break
            except Exception as message:
                self.element_error(item, message)
        return(newresult)

    @handle_inputs(conditional_statement=True)
    def count(self, expression=None):
        newcount = 0
        for item in self._list:
            try:
                if expression(item):
                    newcount += 1
            except Exception as message:
                self.element_error(item, message)
        return(newcount)

    @handle_inputs(conditional_statement=True)
    def distinct(self, expression=None):
        newlist = []
        for item in self._list:
            try:
                if expression(item) and item not in newlist:
                    newlist.append(item)
            except Exception as message:
                self.element_error(item, message)
        return(self.__class__(newlist))

    @handle_inputs(conditional_statement=False)
    def max(self, expression=None):
        newlist = []
        for item in self._list:
            try:
                if isinstance(expression(item),bool) and expression(item) and item not in newlist:
                    newlist.append(item)
                elif not isinstance(expression(item),bool) and expression(item) and item not in newlist:
                    _ = expression(item) > 0 # make sure that all elements can be operated on with > sign.
                    newlist.append(expression(item))
            except Exception as message:
                self.element_error(item, message)
        if not newlist:
            return None
        return(reduce(lambda a,b : a if a > b else b, newlist))

    @handle_inputs(conditional_statement=False)
    def min(self, expression=None):
        newlist = []
        for item in self._list:
            try:
                if isinstance(expression(item),bool) and expression(item) and item not in newlist:
                    newlist.append(item)
                elif not isinstance(expression(item),bool) and expression(item) and item not in newlist:
                    _ = expression(item) < 0 # make sure that all elements can be operated on with < sign.
                    newlist.append(expression(item))
            except Exception as message:
                self.element_error(item, message)
        if not newlist:
            return None
        return(reduce(lambda a,b : a if a < b else b, newlist))

    @handle_inputs(conditional_statement=False)
    def sum(self, expression=None):
        newlist = []
        for item in self._list:
            try:
                if isinstance(expression(item),bool) and expression(item):
                    newlist.append(item)
                elif not isinstance(expression(item),bool) and expression(item):
                    _ = expression(item) + 0 # make sure that all elements can be operated on with + sign.
                    newlist.append(expression(item))
            except Exception as message:
                self.element_error(item, message)
        if not newlist:
            return(None)
        return(reduce(lambda a,b : a+b, newlist))
