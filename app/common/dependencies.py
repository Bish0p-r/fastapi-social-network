from fastapi import Depends

from app.database import get_async_session


ActiveAsyncSession = Depends(get_async_session)
