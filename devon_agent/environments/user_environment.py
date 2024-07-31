import re
import time
from typing import TYPE_CHECKING, Callable

from devon_agent.environment import EnvironmentModule

if TYPE_CHECKING:
    pass


class UserEnvironment(EnvironmentModule):
    user_func: Callable

    @property
    def name(self):
        return "user_environment"

    def setup(self, **kwargs):
        pass

    def teardown(self, **kwargs):
        pass

    def execute(self, input: str, timeout_duration=25):
        self.event_log.append(
            {
                "type": "UserRequest",
                "content": input,
                "producer": "tool",
                "consumer": self.name,
            }
        )
        print("added user request",self.event_log[-1],len(self.event_log))

        response = self.user_func()
        # remove <AGENT> ... </AGENT>
        pattern = r'<AGENT>.*?</AGENT>'
        # Use re.sub() to replace the pattern with an empty string
        cleaned_text = re.sub(pattern, '', response, flags=re.DOTALL)

        self.event_log.append(
            {
                "type": "UserResponse",
                "content": cleaned_text,
                "producer": self.name,
                "consumer": "tool",
            }
        )
        return response

    def save(self):
        return {
            "type": "UserEnvironment",
        }

    def load(self, data, user_func):
        self.user_func = user_func

    @classmethod
    def from_data(cls, data, user_func):
        return cls(user_func=user_func)
