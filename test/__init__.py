from fastapi import status

from config.db import TESTING
from config.utils import LockedError

if not TESTING:
    raise LockedError(
        status_code=status.HTTP_423_LOCKED, detail="To run the tests, you need to set the TESTING variable to True")
