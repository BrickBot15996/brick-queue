from typing import override


class TrackedTeam:
    def __init__(self, teamNumber: int):
        self.teamNumber: int = teamNumber
        self.matchNumbers: list[int] = []
        self.latestMatch: int = 0

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, TrackedTeam):
            return False

        return self.teamNumber == value.teamNumber

if __name__ == '__main__':
    raise RuntimeError('team.py should not be run as main.')
