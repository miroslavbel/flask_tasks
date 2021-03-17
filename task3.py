from enum import IntEnum, auto


class EventType(IntEnum):
    START = auto()
    END = auto()


class EventCreator(IntEnum):
    LESSON = auto()
    PUPIL = auto()
    TUTOR = auto()


class AbsenceEvent:
    def __init__(self, time: int, event_creator: EventCreator, event_type: EventType):
        self.time = time
        self.event_creator = event_creator
        self.event_type = event_type

    def __lt__(self, other):
        """
        a < b

        :param other:
        :return:
        """
        return self.time < other.time

    def __repr__(self):
        return f"<{self.time}: ({self.event_creator.name}, {self.event_type.name})>"


def _fill_set(store_array: list[AbsenceEvent], input_array: list[int], event_creator: EventCreator) -> None:
    """
    Заполняет {@code store_array} событиями.

    :param store_array: массив для заполнения
    :param input_array: массив с датой
    :param event_creator: инициатор события
    """
    for i in range(int(len(input_array) / 2)):
        real_i = i * 2
        start_time = input_array[real_i]
        end_time = input_array[real_i + 1]
        start_event = AbsenceEvent(start_time, event_creator, EventType.START)
        end_event = AbsenceEvent(end_time, event_creator, EventType.END)
        store_array.append(start_event)
        store_array.append(end_event)


def task_3(intervals: dict[str, list[int]]) -> int:
    res = 0
    store_array: list[AbsenceEvent] = []
    _fill_set(store_array, intervals['lesson'], EventCreator.LESSON)
    _fill_set(store_array, intervals['pupil'], EventCreator.PUPIL)
    _fill_set(store_array, intervals['tutor'], EventCreator.TUTOR)
    store_array.sort()
    state_dict = {'isLesson': False, 'isPupil': False, 'isTutor': False}
    time_start = None
    for event in store_array:
        before_event_state = all(key for key in state_dict.values())
        #
        event_type = event.event_type
        event_creator = event.event_creator
        # установка того, что должно быть после события
        value = False
        if event_type == EventType.START:
            value = True
        if event_creator == EventCreator.LESSON:
            state_dict['isLesson'] = value
        elif event_creator == EventCreator.PUPIL:
            state_dict['isPupil'] = value
        elif event_creator == EventCreator.TUTOR:
            state_dict['isTutor'] = value
        #
        after_event_state = all(key for key in state_dict.values())
        if before_event_state != after_event_state:
            if after_event_state:
                # F -> T
                time_start = event.time
            else:
                # T -> F
                res += event.time - time_start
                time_start = None
    return res
