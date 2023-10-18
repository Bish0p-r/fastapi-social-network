from pydantic import BaseModel, EmailStr, validator, field_validator, ValidationError, constr, Field, model_validator


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class UserRegisterSchema(UserLoginSchema):
    first_name: str = Field(min_length=8, max_length=50)
    last_name: str = Field(min_length=8, max_length=50)
    confirm_password: str = Field(min_length=8, max_length=50)

    @model_validator(mode='after')
    def check_passwords_match(self):
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self
