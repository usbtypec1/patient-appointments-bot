from aiogram.fsm.state import State, StatesGroup

__all__ = ('PatientAddStates',)


class PatientAddStates(StatesGroup):
    full_name = State()
    born_on = State()
