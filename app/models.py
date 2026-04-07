from pydantic import BaseModel


class CallbackRequest(BaseModel):
    """Model for customer callback request form."""

    name: str
    phone: str
    email: str | None = None
    message: str | None = None
