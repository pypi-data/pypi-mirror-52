from typing import GenericMeta, List, _ForwardRef
from types import FunctionType
import sip
from PyQt5.QtCore import Qt, QUrl, QObject, Q_CLASSINFO, pyqtSignal, pyqtProperty, pyqtSlot, QTimer
from PyQt5.QtQml import QQmlListProperty, QQmlParserStatus, QQmlContext, QQmlEngine, QQmlComponent, qmlRegisterType
from PyQt5.QtQuick import QQuickItem


propertyClasses = {
    int: int,
    float: float,
    str: 'QString',
    list: list
}

objectRegistry = {}

#
# Type and Registry helpers
#

def findPropertyType(propertyType):
    if type(propertyType) is GenericMeta:
        containerType = propertyType.__orig_bases__[0]
        itemType = propertyType.__args__[0]

        if containerType is not list:
            raise Exception('Only list containers are supported property types')

        if itemType is str:
            return 'QStringList', None

        if itemType in propertyClasses.keys():
            return list, None

        return propertyClasses.get(itemType, itemType), propertyClasses.get(containerType, containerType)

    if type(propertyType) is _ForwardRef:
        propertyType = propertyType.__forward_arg__

    if type(propertyType) is str:
        if propertyType in objectRegistry:
            return objectRegistry[propertyType]

    return propertyClasses.get(propertyType, propertyType), None


def findObjectModule(objectClass):
    if objectClass == type:
        return

    if hasattr(objectClass, '_Module'):
        return objectClass._Module

    return findObjectModule(objectClass.__class__)


def findClassProperties(objectClass, properties={}):
    if objectClass == type:
        return properties

    if type(objectClass) in (tuple, list):
        for objClass in objectClass:
            findClassProperties(objClass, properties)

        return properties

    if hasattr(objectClass, '__properties__'):
        properties.update(objectClass.__properties__)

    return findClassProperties(objectClass.__class__, properties)


def findMethodTypes(objectMethod, className=None):
    annotations = objectMethod.__annotations__
    types = {'return': None, 'args': []}

    for name, typeValue in annotations.items():
        itemType, containerType = findPropertyType(typeValue)

        if name is 'return':
            types['return'] = containerType or itemType
        else:
            types['args'].append(containerType or itemType)

    if types['return'] == className:
        types['return'] = 'QObject'

    return types['args'], types['return']


def createContext(_parent, **contextData):
    context = QQmlContext(QQmlEngine.contextForObject(_parent), _parent)
    context.setContextProperties(contextData)

    return context


def create(_component, _parent, **contextData):
    instance = _component.createObject(_parent)

    context = QQmlContext(Context._RootContext, _parent)
    #context = QQmlContext(QQmlEngine.contextForObject(_parent), _parent)
    instance = _component.create(context)
    for key, val in contextData.items():
        context.setContextProperty(key, val)
        _component.setProperty(key, val)
    instance.setParent(_parent)
    _component.setProperty('parent', _parent)

    return instance


def wrapMethod(obj, key, signal):
    def wrapped(self, *args, **kwargs):
        method(*args, **kwargs)
        signal.emit()

    method = getattr(obj, key)
    setattr(obj, key, wrapped)


def wrapList(value, signal):
    for key in value.__dir__():
        if not key.startswith('__'):
            wrapMethod(value, key, signal)


class ListProperty(list):
    def __init__(self, value):
        list.__init__(self, value)
        self.signal = None
        self.parent = None

    def set_signal(self, signal, parent):
        self.signal = signal
        self.parent = parent

    def clear(self):
        list.clear(self)
        self.signal.emit()

    def extend(self, values):
        list.extend(self, values)
        self.signal.emit()

    def append(self, value):
        list.append(self, value)
        self.signal.emit()

    def remove(self, value):
        list.remove(self, value)
        self.signal.emit()

    def reverse(self):
        list.reverse(self)
        self.signal.emit()

    def insert(self, index, value):
        list.insert(self, index, value)
        self.signal.emit()

    def pop(self, *args):
        list.pop(self, *args)
        self.signal.emit()


#
# Decorators
#


def objectProperty(objectMethod):
    # just tag the method so we can build the property in the metaclass
    objectMethod.__is_object_property__ = True
    return objectMethod


def computedProperty(*deps):
    def wrapper(method):
        method.__computed_property_deps__ = deps
        method.__is_object_property__ = True

        return method

    return wrapper

#
# Object MetaClass
#


class ObjectProperty:
    def __init__(self, name, propertyType, valueName, signalName, signal, classModule):
        self.name = name
        self.valueName = valueName
        self.signalName = signalName
        self.classModule = classModule
        self.signal = signal
        self.itemType, self.containerType = findPropertyType(propertyType)

    def isList(self):
        return self.containerType is not None or self.itemType in ('QStringList', list)

    def buildProperty(self):
        def findItemType(itemType):
            if type(itemType) is _ForwardRef:
                itemType = itemType.__forward_arg__

            if type(itemType) is not str:
                return itemType

            return objectRegistry.get(f'{self.classModule}.{itemType}', itemType)

        def getter(s):
            return getattr(s, self.valueName)

        def setter(s, value):
            setattr(s, self.valueName, value)
            getattr(s, self.signalName).emit()

        def listGetter(s):
            itemType = findItemType(self.itemType)
            value = getattr(s, self.valueName)

            return QQmlListProperty(itemType, s, value)

        if self.containerType is not None:
            containerType = QQmlListProperty if self.containerType is list else self.containerType
            return pyqtProperty(containerType, listGetter, setter, notify=self.signal)

        itemType = findItemType(self.itemType)
        return pyqtProperty(itemType, getter, setter, notify=self.signal, user=True)


class ObjectMetaClass(sip.wrappertype):
    def __new__(cls, name, bases, dct):
        # setup class metadata
        if '_defaultProperty' in dct:
            Q_CLASSINFO('DefaultProperty', dct['_defaultProperty'])

        # create properties from typed class variables (annotations)
        properties = dct['__properties__'] = {}
        computedProperties = dct['__computed_properties__'] = {}
        annotations = dct.get('__annotations__', {})
        for propertyName, propertyType in annotations.items():
            valueName = f'_{propertyName}'
            signalName = f'_{propertyName}Signal'

            dct[valueName] = dct.get(propertyName, None)
            signal = dct[signalName] = pyqtSignal()

            # convert string type references to the current class to QObject
            modules = [findObjectModule(superClass) for superClass in bases]
            module = list(filter(lambda i: i, modules))[0]  # filter out None
            objectProperty = ObjectProperty(propertyName, propertyType, valueName, signalName, signal, module)
            dct[propertyName] = objectProperty.buildProperty()
            properties[propertyName] = objectProperty

            if objectProperty.isList():
                # create a default list if needed
                if dct[valueName] is None:
                    dct[valueName] = []

                dct[valueName] = ListProperty(dct[valueName])

        # add properties from superclasses
        properties.update(findClassProperties(bases, properties))

        # create slots from typed methods
        newItems = {}
        for key, value in dct.items():
            if type(value) is FunctionType and not key.startswith('_') and len(value.__annotations__) > 0:
                argTypes, returnType = findMethodTypes(value, name)
                if hasattr(value, '__is_object_property__'):
                    sig = newItems['_' + key + 'Signal'] = pyqtSignal()
                    dct[key] = pyqtProperty(returnType, notify=sig)(value)
                    if hasattr(value, '__computed_property_deps__'):
                        computedProperties[key] = getattr(value, '__computed_property_deps__')
                else:
                    kwargs = {'result': returnType} if returnType is not None else {}
                    dct[key] = pyqtSlot(*argTypes, **kwargs)(value)

        dct.update(newItems)

        ObjectClass = super().__new__(cls, name, bases, dct)

        if name != 'Object':
            objectRegistry[f'{ObjectClass._Module}.{name}'] = ObjectClass

        return ObjectClass


#
# Object abstract class
#

class Object(QObject, QQmlParserStatus, metaclass=ObjectMetaClass):
    _QmlEngine = None
    _Module = 'Objects'
    _ModuleVersion = (1, 0)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self._parent = parent
        propertyNames = self.__properties__.keys()
        for name, value in kwargs.items():
            if name not in propertyNames:
                raise TypeError(f"__init__() got an unexpected keyword argument: '{name}'")

            setattr(self, name, value)

        # setup slots
        for name in propertyNames:
            value = getattr(self, f'_{name}')
            signal = getattr(self, f'_{name}Signal')
            signal.connect((lambda n: lambda: self.onChanged(n, getattr(self, n)))(name))  # double lambda to create copy of name variable
            upper_name = name[0].upper() + name[1:]
            if hasattr(self, f'on{upper_name}Changed'):
                getattr(self, f'_{name}Signal').connect((lambda un, n: lambda: getattr(self, f'on{un}Changed')(getattr(self, n)))(upper_name, name))

            if isinstance(value, ListProperty):
                value.set_signal(signal, self)

        for name, deps in self.__computed_properties__.items():
            signal = getattr(self, f'_{name}Signal')
            for dep in deps:
                dep_signal = getattr(self, f'_{dep}Signal')
                dep_signal.connect(signal.emit)

        self.onInit()

    def __repr__(self):
        props = []
        for name, objectProperty in self.__properties__.items():
            val = getattr(self, '_' + name)
            valStr = '[...]' if objectProperty.isList() and len(val or []) > 0 else repr(val)
            props.append(f'{name}={valStr}')

        return f'<{self.__class__.__name__} {" ".join(props)}>'

    def classBegin(self):
        pass

    def componentComplete(self):
        pass

    @property
    def qmlEngine(self) -> QQmlEngine:
        return self._QmlEngine

    def propertyValues(self):
        return {name: getattr(self, name) for name in self.__properties__.keys()}

    def copy(self):
        return self.__class__(parent=self._parent, **self.propertyValues())

    def onInit(self):
        pass

    def onChanged(self, propertyName, propertyValue):
        pass

    def changed(self, propertyName):
        getattr(self, f'_{propertyName}Signal').emit()
        self.onChanged(propertyName)

    @objectProperty
    def className(self) -> str:
        return self.__class__.__name__

    @objectProperty
    def displayClassName(self) -> str:
        return getattr(self, '_DisplayClassName', self.className)

    @objectProperty
    def propertyNames(self) -> List[str]:
        return self.__properties__.keys()

    def on_timeout(self, seconds, callback):
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(callback)
        timer.start(seconds * 1000)

    def on_interval(self, seconds, callback):
        timer = QTimer(self)
        timer.timeout.connect(callback)
        timer.start(seconds * 1000)

#
# Helper classes
#

class Context(QQmlContext):
    _RootContext = None

    def __init__(self, _parent, **data):
        parentContext = QQmlEngine.contextForObject(_parent)
        super().__init__(parentContext, _parent)

        for key, val in data.items():
            self.setContextProperty(key, val)


#
# Setup
#

def registerQmlTypes():
    for module, ObjectClass in objectRegistry.items():
        version = ObjectClass._ModuleVersion
        qmlRegisterType(ObjectClass, ObjectClass._Module, version[0], version[1], ObjectClass.__name__)


def registerRootContext(rootContext):
    Context._RootContext = rootContext
    Object._QmlEngine = rootContext.engine()
