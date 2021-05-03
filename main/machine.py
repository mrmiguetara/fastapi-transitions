from transitions.extensions import GraphMachine as Machine
from functools import partial

class UserStatus():
    INITIAL = 'solid'
    STATES = [
        'solid',
        'liquid',
        'gas',
        'plasma'
    ]

    TRANSITIONS = [
        { 'trigger': 'melt', 'source': 'solid', 'dest': 'liquid' },
        { 'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas' },
        { 'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas' },
        { 'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma' }
    ]    
    @classmethod
    def get_kwargs(cls):
        """Get the kwargs to initialize the state machine."""
        kwargs = {
            'states': cls.STATES,
            'transitions': cls.TRANSITIONS,
        }
        return kwargs

class UserMachineMixin(object):
    """
    Base class for state machine mixins.
    Class attributes:
    * ``status_class`` must provide ``TRANSITION_LABELS`` property
      and the ``get_kwargs`` class method (see ``StatusBase``).
    * ``machine`` is a transition machine e.g::
        machine = Machine(
            model=None,
            finalize_event='wf_finalize',
            auto_transitions=False,
            **status_class.get_kwargs()  # noqa: C815
        )
    The transition events of the machine will be added as methods to
    the mixin.
    """
    status_class = UserStatus
    machine = Machine(
        model=None,
        **status_class.get_kwargs(),
    )

    def __init__(self, **kwargs):
        super(UserMachineMixin, self).__init__(**kwargs)
        self.machine.add_model(self)
    @property
    def state(self):
        """Get the items workflowstate or the initial state if none is set."""
        if self.user_state:
            return self.user_state
        return self.machine.initial

    @state.setter
    def state(self, value):
        """Set the items workflow state."""
        self.user_state = value
        # tasks.test_task.delay(new_state=value)
        return self.user_state

    
    def init_machine(self):
        if not self in self.machine.models:
            self.machine.add_model(self, self.user_state)
        return

    def __getattribute__(self, item):
        """Propagate events to the workflow state machine."""
        try:
            return super(UserMachineMixin, self).__getattribute__(item)
        except AttributeError:
            if item in self.machine.events:
                return partial(self.machine.events[item].trigger, self)
            raise
