from __future__ import absolute_import

import six

from sentry.grouping.flavors import get_event_flavor_keys


registered_strategies = {}


class StrategyVersion(object):

    def __init__(self, strategy_class, identifier, version, priority, flavors):
        self.strategy_class = strategy_class
        self.identifier = identifier
        self.version = version
        self.priority = priority
        self.flavors = flavors

    def is_applicable(self, data, flavor_keys):
        for flavor_key in flavor_keys:
            if flavor_key in self.flavors:
                return self.strategy_class.is_applicable_for_data(data)
        return False


def register_strategy(identifier, version, priority=100, flavors=None):
    if not flavors:
        flavors = ['platform:generic']

    def decorator(cls):
        full_id = '%s:%s' % (identifier, version)
        registered_strategies[full_id] = StrategyVersion(
            strategy_class=cls,
            identifier=identifier,
            version=version,
            priority=priority,
            flavors=flavors
        )
        return cls
    return decorator


class Strategy(object):

    @classmethod
    def is_applicable_for_data(cls, data):
        return False


def get_used_project_strategies(project, flavor_keys):
    # So far we don't support this
    return {}


def get_applicable_strategies(data, flavor_keys=None):
    if flavor_keys is None:
        flavor_keys = get_event_flavor_keys(data)
    rv = []
    for strategy_version in six.itervalues(registered_strategies):
        if strategy_version.is_applicable(data, flavor_keys):
            rv.append((strategy_version.identifier, strategy_version.version))
    return rv


class StrategyConfig(object):

    def __init__(self, project, flavor_keys, old_strategies=None,
                 new_strategies=None):
        self.project = project
        self.flavor_keys = flavor_keys
        self.old_strategies = old_strategies
        self.new_strategies = new_strategies

    def iter_strategies(self):
        for item in self.old_strategies or ():
            yield item
        for item in self.new_strategies or ():
            yield item


def pick_strategies(project, data):
    """Given a project and the data this returns a list of strategy
    configurations that should be tested.  This might use frozen
    information based on if a flavor keys were used previously.
    """
    flavor_keys = get_event_flavor_keys(data)
    used_strategies = get_used_project_strategies(project, flavor_keys)
    applicable_strategies = get_applicable_strategies(data, flavor_keys)

    old_strategies = []
    new_strategies = []

    for strategy_id, preferred_version in applicable_strategies:
        old_version = used_strategies.get(strategy_id)
        if old_version is not None:
            old_strategies.append((strategy_id, old_version))
        else:
            new_strategies.append((strategy_id, preferred_version))

    return StrategyConfig(
        project=project,
        flavor_keys=flavor_keys,
        old_strategies=old_strategies,
        new_strategies=new_strategies
    )
