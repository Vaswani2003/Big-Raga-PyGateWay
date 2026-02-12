from enum import Enum

class OSPlatform(str, Enum):
    WIN32: str = "win32"
    LINUX: str = "linux"
    DARWIN: str = "darwin"