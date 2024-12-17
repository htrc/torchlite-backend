from importlib.metadata import version, PackageNotFoundError

try:
    VERSION = version("torchlite")
except PackageNotFoundError:
    VERSION = "UNKNOWN"
