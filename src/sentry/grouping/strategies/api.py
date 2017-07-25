from __future__ import absolute_import

import six

from contextlib import contextmanager
from itertools import chain
from weakref import ref as weakref

from sentry.interfaces.base import get_interface
from sentry.grouping.flavors import get_event_flavor_keys


registered_strategies = {}
strategies_by_priority = []
LATEST_STRATEGIES = {}


def _parse_version(version):
    return tuple(map(int, version.split('.')))


class StrategyNotFound(LookupError):
    pass


class StrategyVersion(object):

    def __init__(self, strategy_class, identifier, version, priority, flavors,
                 description):
        self.strategy_class = strategy_class
        self.strategy = strategy_class(self)
        self.identifier = identifier
        self.version = version
        self.priority = priority
        self.flavors = flavors
        self.description = description

    @property
    def full_id(self):
        return '%s:%s' % (self.identifier, self.version)

    def get_applicable_flavor(self, data, flavor_keys):
        for flavor_key in flavor_keys:
            if flavor_key in self.flavors and \
               self.strategy_class.is_applicable_for_data(data):
                return flavor_key
        return None


def register_strategy(identifier, version, priority=100, flavors=None,
                      description=None):
    if not flavors:
        flavors = ['platform:generic']

    def decorator(cls):
        v = StrategyVersion(
            strategy_class=cls,
            identifier=identifier,
            version=version,
            priority=priority,
            flavors=flavors,
            description=description,
        )

        old_version = LATEST_STRATEGIES.get(identifier)
        if old_version is None or \
           _parse_version(old_version) < _parse_version(version):
            LATEST_STRATEGIES[identifier] = version

        registered_strategies[v.full_id] = v
        strategies_by_priority.append(v)
        strategies_by_priority.sort(key=lambda x: x.priority)
        return cls
    return decorator


class Strategy(object):

    def __init__(self, version):
        self._version = weakref(version)

    @property
    def version(self):
        rv = self._version()
        if rv is None:
            raise AttributeError('version')
        return rv

    @classmethod
    def is_applicable_for_data(cls, data):
        return False


def get_used_project_strategy_versions(project, flavor_keys):
    """Returns the already used project strategy configs.  The
    return value is a dictionary keyed by the flavor key and a
    dictionary of 'strategy' -> 'version' mapping.  Without a
    flavor all strategies have the same version even if used
    nested.
    """
    return {}


def get_applicable_strategies(data, flavor_keys=None):
    if flavor_keys is None:
        flavor_keys = get_event_flavor_keys(data)
    rv = []
    # XXX: ony pick applicable version
    for strategy_version in strategies_by_priority:
        flavor_key = strategy_version.get_applicable_flavor(data, flavor_keys)
        if flavor_key is not None:
            rv.append((strategy_version.identifier,
                       strategy_version.version,
                       flavor_key))
    return rv


def get_latest_strategy_version(identifier):
    return LATEST_STRATEGIES.get(identifier)


class StrategyPick(object):

    def __init__(self, project, flavor_keys, platform,
                 used_strategy_versions, old_strategies, new_strategies):
        self.project = project
        self.flavor_keys = flavor_keys
        self.platform = platform
        self.used_strategy_versions = used_strategy_versions
        self.old_strategies = old_strategies
        self.new_strategies = new_strategies

    def find_strategy_version(self, identifier, flavor_key, preferred_version=None):
        # IF we already used a version of the strategy for the current
        # flavor_key, we used that under all circumstances
        versions = self.used_strategy_versions.get(flavor_key)
        if versions is not None:
            version = versions.get(identifier)
            if version is not None:
                return version

        # support getting the latest version
        if preferred_version is None:
            preferred_version = 'latest'
        if preferred_version == 'latest':
            return get_latest_strategy_version(identifier)

        # look up a specific version
        full_id = '%s:%s' % (identifier, preferred_version)
        if registered_strategies.get(full_id) is not None:
            return preferred_version

    def find_strategy(self, identifier, flavor_key, preferred_version=None):
        version = self.find_strategy_version(identifier, preferred_version)
        if version is None:
            raise StrategyNotFound(identifier)
        full_id = '%s:%s' % (identifier, version)
        return registered_strategies[full_id]

    def process_interfaces(self, interfaces, all=False):
        """Processes the interfaces with the best picked strategy."""
        hasher = GroupHasher(self)
        iterator = chain(self.old_strategies, self.new_strategies)
        rv = []

        for identifier, version, flavor_key in iterator:
            obj = hasher.hash_interfaces(
                identifier, version, flavor_key, interfaces)
            if obj is not None:
                if not all:
                    return obj
                rv.append(obj)

        if all:
            return rv

    def process_event(self, event, all=False):
        """Processes an event with the best picked strategy."""
        return self.process_interfaces(event.get_interfaces(), all=all)

    def process_data(self, data, all=False):
        """Processes event data with the best picked strategy."""
        interfaces = {}
        for key, value in six.iteritems(data):
            try:
                interface_cls = get_interface(key)
            except ValueError:
                continue
            interface = interface_cls()
            interfaces[interface.get_path()] = interface.to_python(value)
        return self.process_interfaces(interfaces, all=all)


class GroupHasher(object):

    def __init__(self, pick):
        self.stack = []
        self.pick = pick

    @property
    def current_object(self):
        try:
            return self.stack[-1][2]
        except IndexError:
            return None

    @property
    def current_flavor_key(self):
        try:
            return self.stack[-1][1]
        except IndexError:
            return None

    @property
    def current_strategy_version(self):
        try:
            return self.stack[-1][0]
        except IndexError:
            return None

    @property
    def did_contribute(self):
        obj = self.current_object
        return bool(obj and (obj['values'] or obj['nested']))

    def enter_strategy(self, strategy_version, flavor_key):
        obj = {
            'strategy': strategy_version.full_id,
            'values': [],
            'nested': [],
        }
        cur_obj = self.current_object
        if cur_obj is not None:
            cur_obj['nested'].append(obj)
        self.stack.append((strategy_version, flavor_key, obj))
        return obj

    def leave_strategy(self):
        self.stack.pop()

    @contextmanager
    def nested_strategy(self, strategy_version, flavor_key):
        obj = self.enter_strategy(strategy_version, flavor_key)
        try:
            yield obj
        finally:
            self.leave_strategy()

    def contribute_value(self, value):
        """Contributes a single value to the hasher"""
        if isinstance(value, (tuple, list)):
            for value in value:
                self.contribute_value(value)
        else:
            self.current_object['values'].append(value)

    def contribute_nested(self, identifier, interfaces,
                          preferred_version=None):
        """Contributes a nested strategy to the hasher."""
        flavor_key = self.current_flavor_key
        strategy_version = self.pick.find_strategy(
            identifier, flavor_key, preferred_version)
        with self.nested_strategy(strategy_version, flavor_key):
            strategy_version.strategy.hash_interfaces(
                interfaces=interfaces,
                platform=self.pick.platform,
                hasher=self
            )

    def hash_interfaces(self, identifier, version, flavor_key, interfaces):
        """Tells the hasher to hash a specific strategy for a flavor."""
        try:
            strategy_version = self.pick.find_strategy(
                identifier, version, flavor_key)
        except StrategyNotFound:
            return
        obj = self.enter_strategy(strategy_version, flavor_key)
        strategy_version.strategy.hash_interfaces(
            interfaces=interfaces,
            platform=self.pick.platform,
            hasher=self
        )
        did_contribute = self.did_contribute
        self.leave_strategy()
        if did_contribute:
            return obj


def pick_strategies(project, data):
    """Given a project and the data this returns a list of strategy
    configurations that should be tested.  This might use frozen
    information based on if a flavor keys were used previously.

    Usage::

        from sentry.grouping.strategies.api import pick_strategies
        pick = pick_strategies(project, data)
        # later
        hash_info = pick.process_interfaces(interfaces)

    Or if you want all hashes::

        hash_infos = pick.process_interfaces(interfaces, all=True)

    The creation of the strategies is based on the raw event data
    wheras the processing takes places on the interfaces.
    """
    flavor_keys = get_event_flavor_keys(data)
    used_strategy_versions = get_used_project_strategy_versions(
        project, flavor_keys)
    applicable_strategies = get_applicable_strategies(data, flavor_keys)

    old_strategies = []
    new_strategies = []

    for strategy_id, preferred_version, flavor_key in applicable_strategies:
        old_version = used_strategy_versions.get(
            flavor_key, {}).get(strategy_id)
        if old_version is not None:
            old_strategies.append((strategy_id, old_version, flavor_key))
        else:
            new_strategies.append((strategy_id, preferred_version, flavor_key))

    return StrategyPick(
        project=project,
        flavor_keys=flavor_keys,
        platform=data.get('platform'),
        used_strategy_versions=used_strategy_versions,
        old_strategies=old_strategies,
        new_strategies=new_strategies
    )


def describe_strategy_grouping(values, as_text=False):
    """Given the values from running a strategy over an event this
    returns a human readable version of it.
    """

    def _describe(d):
        strategy_version = registered_strategies.get(d['strategy'])
        if strategy_version is None:
            rv = {
                'strategy': None,
                'description': 'unknown legacy grouping',
            }
        else:
            rv = {
                'strategy': strategy_version.identifier,
                'description': strategy_version.description,
            }

        for nested in d['nested']:
            rv.setdefault('nested', []).append(_describe(nested))

        return rv

    rv = _describe(values)

    if not as_text:
        return rv

    lines = []

    def _dump(value, depth=0):
        lines.append('%s%s %s' % (
            '  ' * depth,
            depth == 0 and 'group by' or 'considering',
            value['description'],
        ))
        for nested in value.get('nested') or ():
            _dump(nested, depth + 1)

    _dump(rv)

    return '\n'.join(lines)
