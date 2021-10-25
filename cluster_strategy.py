from dataclasses import dataclass
import habits
import copy


@dataclass
class ClusterStrategyOptions:
    example: int


class ClusterStrategy:
    def __init__(self, options: ClusterStrategyOptions):
        self.options_ = copy.copy(options)

    def accepts_habit(self, habit):
        return True
