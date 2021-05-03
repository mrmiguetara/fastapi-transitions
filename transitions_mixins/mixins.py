from transitions import Machine
from functools import partial

class MachineStatus(object):
    INITIAL = ''
    STATES = []

    TRANSITIONS = []

    @classmethod
    def get_kwargs(cls):
        kwargs = {
            'initial': cls.INITIAL,
            'states': cls.STATES,
            'transitions': cls.TRANSITIONS,
        }
        return kwargs

class MachineMixin(object):
    status_class = None
    machine = None

    def __init__(self, **kwargs):
        super(MachineMixin, self).__init__(**kwargs)
        self.machine.add_model(self)

    @property
    def state(self):
        return

    @state.setter
    def state(self, value):
        return

    def init_machine(self):
        if not self in self.machine.models:
            self.machine.add_model(self, self.user_state)
        return

    def __getattribute__(self, item):
        try:
            return super(MachineMixin, self).__getattribute__(item)
        except AttributeError:
            if item in self.machine.events:
                return partial(self.machine.events[item].trigger, self)
            raise
