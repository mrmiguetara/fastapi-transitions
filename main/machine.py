from transitions.extensions import GraphMachine as Machine
from functools import partial
from transitions_mixins.mixins import MachineMixin, MachineStatus

class UserStatus(MachineStatus):
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
class UserMachineMixin(MachineMixin):
    status_class = UserStatus
    machine = Machine(
        model=None,
        **status_class.get_kwargs(),
    )

    @property
    def state(self):
        if self.user_state:
            return self.user_state
        return self.machine.initial

    @state.setter
    def state(self, value):
        self.user_state = value
        return self.user_state

