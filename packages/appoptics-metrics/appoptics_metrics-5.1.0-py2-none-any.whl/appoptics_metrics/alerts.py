class Alert(object):
    """AppOptics Alert Base class"""

    def __init__(self, connection, name, _id=None, description=None, version=2, md=False,
                 conditions=None, services=None, attributes=None, active=True, rearm_seconds=None,
                 created_at=None, updated_at=None, rearm_per_signal=None):
        conditions = conditions or []
        services = services or []
        attributes = attributes or {}

        self.connection = connection
        self.name = name
        self.description = description
        self.version = version
        self.conditions = []
        for c in conditions:
            if isinstance(c, Condition):
                self.conditions.append(c)
            elif isinstance(c, dict):
                self.conditions.append(Condition.from_dict(c))
            else:
                self.conditions.append(Condition(*c))
        self.services = []
        for s in services:
            if isinstance(s, Service):
                self.services.append(s)
            elif isinstance(s, dict):
                self.services.append(Service.from_dict(connection, s))
            elif isinstance(s, int):
                self.services.append(Service(s))
            else:
                self.services.append(Service(*s))
        self.attributes = attributes
        self.active = active
        self.rearm_seconds = rearm_seconds
        self._id = _id
        self.md = md
        self.created_at = created_at
        self.updated_at = updated_at
        self.rearm_per_signal = rearm_per_signal

    def add_condition_for(self, metric_name, source='*'):
        condition = Condition(metric_name, source)
        self.conditions.append(condition)
        return condition

    def add_service(self, service_id):
        self.services.append(Service(service_id))

    def __repr__(self):
        return "%s<%s>" % (self.__class__.__name__, self.name)

    @classmethod
    def from_dict(cls, connection, data):
        """Returns an alert object from a dictionary item,
        which is usually from AppOptics's API"""
        obj = cls(connection,
                  data.get('name'),
                  version=data.get('version'),
                  description=data.get('description'),
                  conditions=data.get('conditions'),
                  services=data.get('services'),
                  _id=data.get('id'),
                  active=data.get('active'),
                  rearm_seconds=data.get('rearm_seconds'),
                  attributes=data.get('attributes'),
                  md=data.get('md'),
                  created_at=data.get('created_at'),
                  updated_at=data.get('updated_at'),
                  rearm_per_signal=data.get('rearm_per_signal')
                  )
        return obj

    def get_payload(self):
        return {'name': self.name,
                'md': self.md,
                'id': self._id,
                'attributes': self.attributes,
                'version': self.version,
                'description': self.description,
                'rearm_seconds': self.rearm_seconds,
                'active': self.active,
                'services': [x._id for x in self.services],
                'conditions': [x.get_payload() for x in self.conditions],
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'rearm_per_signal': self.rearm_per_signal,
                }

    def save(self):
        self.connection.update_alert(self)


class Condition(object):
    ABOVE = 'above'
    BELOW = 'below'
    ABSENT = 'absent'

    # Note this is 'average' not 'mean'
    SUMMARY_FUNCTION_AVERAGE = 'average'

    def __init__(self, metric_name, source='*', tags=None):
        self.metric_name = metric_name
        self.source = source
        self.tags = tags or []
        self.summary_function = None

    def above(self, threshold, summary_function=SUMMARY_FUNCTION_AVERAGE):
        self.condition_type = self.ABOVE
        self.summary_function = summary_function
        self.threshold = threshold
        # This implies an immediate trigger
        self._duration = None
        return self

    def below(self, threshold, summary_function=SUMMARY_FUNCTION_AVERAGE):
        self.condition_type = self.BELOW
        self.summary_function = summary_function
        self.threshold = threshold
        # This implies an immediate trigger
        self._duration = None
        return self

    # Stops reporting for a duration (in seconds)
    def stops_reporting_for(self, duration):
        self.condition_type = self.ABSENT
        self.summary_function = None
        self._duration = duration
        return self

    def duration(self, duration):
        self._duration = duration

    # An alert condition is either "immediate" or "time windowed"
    def immediate(self):
        if self._duration is None or self._duration == 0:
            return True
        else:
            return False

    @classmethod
    def from_dict(cls, data):
        obj = cls(metric_name=data['metric_name'],
                  source=data.get('source', '*'),
                  tags=data.get('tags', []))
        if data['type'] == Condition.ABOVE:
            obj.above(data.get('threshold'), data.get('summary_function'))
            obj.duration(data.get('duration'))
        elif data['type'] == Condition.BELOW:
            obj.below(data.get('threshold'), data.get('summary_function'))
            obj.duration(data.get('duration'))
        elif data['type'] == Condition.ABSENT:
            obj.stops_reporting_for(data.get('duration'))
        return obj

    def get_payload(self):
        obj = {
            'type': self.condition_type,
            'metric_name': self.metric_name,
            'source': self.source,
            'tags': self.tags,
            'summary_function': self.summary_function,
            'duration': self._duration
        }
        if self.condition_type in [self.ABOVE, self.BELOW]:
            obj['threshold'] = self.threshold
        return obj


class Service(object):
    def __init__(self, _id, title=None, type=None, settings=None):
        self._id = _id
        self.title = title
        self.type = type
        self.settings = settings

    @classmethod
    def from_dict(cls, connection, data):
        obj = cls(data['id'], data['title'], data['type'], data['settings'])
        return obj

    def get_payload(self):
        return {
            'id': self._id,
            'title': self.title,
            'type': self.type,
            'settings': self.settings
        }

    def __repr__(self):
        return "%s<%s><%s>" % (self.__class__.__name__, self.type, self.title)
