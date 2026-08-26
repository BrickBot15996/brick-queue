from typing import override

from classes.team import TrackedTeam


class TrackedEvent:
    def __init__(self, eventCode: str):
        self.eventCode: str = eventCode
        self.fieldCount: int = 1
        self.latestMatch: int = 0
        self.trackedTeamsAtEvent: set[TrackedTeam] = set()

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, TrackedEvent):
            return False

        return self.eventCode == value.eventCode

if __name__ == '__main__':
    raise RuntimeError('event.py should not be run as main.')
