# License (MIT License)
#
# Copyright (c) 2007-2008 Christian Schubert and Michael Perscheid
# michael.perscheid@hpi.uni-potsdam.de, http://www.hpi.uni-potsdam.de/swa/
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys, threading, types, operator

__all__ = ['layer']
__all__ += ['activelayer', 'activelayers', 'inactivelayer', 'inactivelayers']
__all__ += ['proceed']
__all__ += ['before', 'after', 'around', 'base']
__all__ += ['globalActivateLayer', 'globalDeactivateLayer']

__version__ = "1.1"

try:
    from __pypy__ import _promote as promote
except ImportError:
    promote = lambda x: x



class MyTLS(threading.local):
    def __init__(self):
        self.context = None
        self.activelayers = layerstack(())

    def get_activelayers(self):
        return self._activelayers

    def set_activelayers(self, new):
        assert isinstance(new, layerstack)
        self._activelayers = new

    activelayers = property(get_activelayers, set_activelayers)


class layer(object):
    def __init__(self, name = None):
        if name:
            self._name = name
            self._unique_id = name + hex(id(self))
        else:
            self._name = self._unique_id = hex(id(self))

    def __str__(self):
        return "<layer %s>" % (self._name)

    def __repr__(self):
        args = []
        if self._name != hex(id(self)):
            args.append('name="%s"' % self._name)
        return "layer(%s)" % (", ".join(args))

    def getEffectiveLayers(self, activelayers):
        return activelayers

_stack_cache = {}

class layerstack(tuple):
    def __new__(cls, layers):
        layers = tuple.__new__(cls, layers)
        return _stack_cache.setdefault(layers, layers)

    def __add__(self, other):
        return layerstack(tuple.__add__(self, other))

_baselayer = layer("no_layer")
# tuple with layers that are always active
_baselayers = layerstack((_baselayer,))

_tls = MyTLS()

class _LayerManager(object):
    def __init__(self, layers):
        self._layers = layers
        self._oldLayers = ()

    def _getActiveLayers(self):
        return self._oldLayers

    def __enter__(self):
        self._oldLayers = _tls.activelayers
        _tls.activelayers = layerstack(self._getActiveLayers())

    def __exit__(self, exc_type, exc_value, exc_tb):
        _tls.activelayers = self._oldLayers

class _LayerActivationManager(_LayerManager):
    def _getActiveLayers(self):
        return [layer for layer in self._oldLayers if layer not in self._layers] + self._layers

class _LayerDeactivationManager(_LayerManager):
    def _getActiveLayers(self):
        return [layer for layer in self._oldLayers if layer not in self._layers]

def activelayer(layer):
    return _LayerActivationManager([layer])

def inactivelayer(layer):
    return _LayerDeactivationManager([layer])

def activelayers(*layers):
    return _LayerActivationManager(list(layers))

def inactivelayers(*layers):
    return _LayerDeactivationManager(list(layers))

def itemgetter_0(obj):
    return obj[0]

def itemgetter_1(obj):
    return obj[1]

def itemgetter_2(obj):
    return obj[2]

def itemgetter_3(obj):
    return obj[3]

def itemgetter_4(obj):
    return obj[4]

class _context(tuple):
    __slots__ = ()

    def __new__(kls, inst, cls, next):
        return tuple.__new__(kls, (inst, cls, next))

    inst = property(itemgetter_0)
    cls = property(itemgetter_1)
    next = property(itemgetter_2)



class _advice(tuple):
    __slots__ = ()

    def __new__(cls, func, next):
        return tuple.__new__(cls, (func, next))

    _func = property(itemgetter_0)
    _next = property(itemgetter_1)

    def _invoke(self, context, args, kwargs):
        if ((context.inst is None) and (context.cls is None)):
            # Normal Python function no binding needed
            return self._func(*args, **kwargs)
        # Kind of instance method, class or static mehtod (binding needed)
        return self._func.__get__(context.inst, context.cls)(*args, **kwargs)

    def __call__(self, context, args, kwargs):
        raise NotImplementedError

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self._func, self._next)

    @classmethod
    def createchain(cls, methods):
        if not methods:
            return _stop(None, None)
        method, when = methods[0]
        return when(method, cls.createchain(methods[1:]))

class _before(_advice):
    __slots__ = ()
    def __call__(self, context, args, kwargs):
        self._invoke(context, args, kwargs)
        return self._next(context, args, kwargs)

class _around(_advice):
    __slots__ = ()
    def __call__(self, context, args, kwargs):
        backup = _tls.context
        context = _context(context.inst, context.cls, self._next)
        _tls.context = context
        result = self._invoke(context, args, kwargs)
        _tls.context = backup
        return result

class _after(_advice):
    __slots__ = ()
    def __call__(self, context, args, kwargs):
        result = self._next(context, args, kwargs)
        kwargs_with_result = dict(__result__ = result, **kwargs)
        return self._invoke(context, args, kwargs_with_result)

class _stop(_advice):
    __slots__ = ()
    def __call__(self, context, args, kwargs):
        raise Exception, "called proceed() in innermost function, this probably means that you don't have a base method (`around` advice in None layer) or the base method itself calls proceed()"

def proceed(*args, **kwargs):
    context = _tls.context
    return context.next(context, args, kwargs)

def _true(activelayers):
    return True

class _layeredmethodinvocationproxy(object):
    __slots__ = ("_inst", "_cls", "_descriptor")

    def __init__(self, descriptor, inst, cls):
        self._inst = inst
        self._cls = cls
        self._descriptor = descriptor

    def __call__(self, *args, **kwargs):
        advice = self._descriptor.get_or_build_methods()

        context = _context(self._inst, self._cls, None)
        result = advice(context, args, kwargs)
        return result

    def getMethods(self):
        return self._descriptor.methods

    def setMethods(self, methods):
        self._descriptor.methods = methods

    def getName(self):
        return self._descriptor.methods[-1][1].__name__

    def registerMethod(self, f, when = _around, layer_ = None, guard = _true):
        self._descriptor.registerMethod(f, when, layer_, guard)

    def unregisterMethod(self, f, layer_ = None):
        self._descriptor.unregisterMethod(f, layer_)

    methods = property(getMethods, setMethods)
    __name__ = property(getName)

class _layeredmethoddescriptor(object):
    def __init__(self, methods):
        self._methods = []
        self._cache = {}
        self.methods = methods
        self.last_activelayers = None
        self.last_baselayers = None
        self.last_advice = None

    def _clearCache(self):
        for key in self._cache.keys():
            self._cache.pop(key, None)

    def cacheMethods(self, activelayers):
        layers = list(activelayers)
        for layer_ in activelayers:
            if layer_ is not None:
                layers = layer_.getEffectiveLayers(layers)

        # For each active layer, get all methods and the when advice class related to this layer
        methods = []
        for currentlayer in reversed(layers):
            for lmwgm in reversed(self._methods):
                if lmwgm.layer is currentlayer and lmwgm.guard(activelayers):
                    methods.append((lmwgm.function, lmwgm.when))

        self._cache[activelayers] =    result = _advice.createchain(methods)
        return result

    def get_or_build_methods(self):
        if self.last_activelayers is _tls.activelayers and self.last_baselayers is _baselayers:
            return promote(self.last_advice)
        activelayers = _baselayers + _tls.activelayers
        advice = self._cache.get(activelayers) or self.cacheMethods(activelayers)
        self.last_activelayers = _tls.activelayers
        self.last_baselayers = _baselayers
        self.last_advice = advice
        return advice

    def setMethods(self, methods):
        for meth in methods:
            assert isinstance(meth, CopMethod)
        self._methods[:] = methods
        self._clearCache()

    def getMethods(self):
        return list(self._methods)

    def registerMethod(self, f, when = _around, layer_ = None, guard = _true, methodName = ""):
        if (methodName == ""):
            methodName = f.__name__
        if hasattr(when, "when"):
            when = when.when

        assert isinstance(layer_, (layer, types.NoneType))
        assert issubclass(when, _advice)

        self.methods = self.methods + [
            CopMethod(layer_, f, when, guard, methodName)]

    def unregisterMethod(self, f, layer_ = None):
        self.methods = [lmwgm for lmwgm in self._descriptor.methods if
            lmwgm.function is not f or lmwgm.layer is not layer_]

    methods = property(getMethods, setMethods)

    def __get__(self, inst, cls = None):
        return _layeredmethodinvocationproxy(self, inst, cls)

    # Used only for functions (no binding or invocation proxy needed)
    def __call__(self, *args, **kwargs):
        advice = self.get_or_build_methods()

        # 2x None to identify: do not bind this function
        context = _context(None, None, None)
        result = advice(context, args, kwargs)
        return result

class CopMethod(tuple):
    def __new__(cls, layer, f, when, guard, methodName=""):
        assert layer is not None
        return tuple.__new__(cls, (layer, f, when, guard, methodName))

    layer = property(itemgetter_0)
    function = property(itemgetter_1)
    when = property(itemgetter_2)
    guard = property(itemgetter_3)
    name = property(itemgetter_4)


def createlayeredmethod(base, partial):
    if base:
        return _layeredmethoddescriptor([CopMethod(_baselayer, base, _around, _true)] + partial)
    else:
        return _layeredmethoddescriptor(partial)

# Needed for a hack to get the name of the class/static method object
class _dummyClass:
    pass

def getMethodName(method):
    if (type(method) in (classmethod, staticmethod)):
        # Bound the method to a dummy class to retrieve the original name
        return method.__get__(None, _dummyClass).__name__
    else:
        return method.__name__

def __common(layer_, guard, when):
    assert isinstance(layer_, (layer, types.NoneType)), "layer_ argument must be a layer instance or None"
    assert callable(guard), "guard must be callable"
    assert issubclass(when, _advice)

    vars = sys._getframe(2).f_locals

    def decorator(method):
        methodName = getMethodName(method)
        currentMethod = vars.get(methodName)
        if (issubclass(type(currentMethod), _layeredmethoddescriptor)):
            #Append the new method
            currentMethod.registerMethod(method, when, layer_, guard, methodName)
        else:
            currentMethod = createlayeredmethod(currentMethod, [CopMethod(layer_, method, when, guard, methodName)])
        return currentMethod

    return decorator

def before(layer_ = None, guard = _true):
    return __common(layer_, guard, _before)
def around(layer_ = None, guard = _true):
    return __common(layer_, guard, _around)
def after(layer_ = None, guard = _true):
    return __common(layer_, guard, _after)

def base(method):
    # look for the current entry in the __dict__ (class or module)
    vars = sys._getframe(1).f_locals
    methodName = getMethodName(method)
    currentMethod = vars.get(methodName)
    if (issubclass(type(currentMethod), _layeredmethoddescriptor)):
        # add the first entry of the layered method with the base entry
        currentMethod.methods = [CopMethod(_baselayer, method, _around, _true)] + currentMethod.methods
        return currentMethod
    return method

before.when = _before
around.when = _around
after.when = _after

def globalActivateLayer(layer):
    global _baselayers
    if layer in _baselayers:
        raise ValueError("layer is already active")
    _baselayers += (layer,)
    return _baselayers

def globalDeactivateLayer(layer):
    global _baselayers
    t = list(_baselayers)
    if layer not in t:
        raise ValueError("layer is not active")
    i = t.index(layer)
    _baselayers = layerstack(t[:i] + t[i+1:])
    return _baselayers
