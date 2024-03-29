from pydantic import BaseModel, EmailStr, Field, model_validator


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class UserRegisterSchema(UserLoginSchema):
    confirm_password: str = Field(min_length=8, max_length=50)
    first_name: str = Field(min_length=8, max_length=50)
    last_name: str = Field(min_length=8, max_length=50)

    @model_validator(mode="after")
    def check_passwords_match(self):
        pw1 = self.password
        pw2 = self.confirm_password

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return self


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class EmailSchema(BaseModel):
    email: EmailStr
