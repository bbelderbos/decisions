
from pydantic import BaseModel, EmailStr, SecretStr
from pydantic import Field as PydanticField


class LoginForm(BaseModel):
    email: EmailStr = PydanticField(
        title="Email Address", description="Try 'x@y' to trigger server side validation"
    )
    password: SecretStr


