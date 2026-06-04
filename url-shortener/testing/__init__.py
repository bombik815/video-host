from os import getenv


class TestingEnvironmentError(OSError):
    def __init__(self) -> None:
        super().__init__("Set TESTING=1 before running tests")


def ensure_testing_environment() -> None:
    if getenv("TESTING") != "1":
        raise TestingEnvironmentError


ensure_testing_environment()
