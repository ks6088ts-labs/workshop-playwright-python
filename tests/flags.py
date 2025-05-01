from os import getenv

SKIP = getenv("SKIP_TEST", "true").lower() == "true"
