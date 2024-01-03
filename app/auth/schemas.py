from pydantic import BaseModel, EmailStr, Field

import settings


class AuthDetails(BaseModel):
    name: str = Field(min_length=settings.Settings.MIN_PASSWORD_LENGTH, max_length=50, examples=['Barak'])
    second_name: str = Field(min_length=2, max_length=50, examples=['Abama'])
    login: EmailStr = Field(examples=['login@ukr.net'])
    password: str = Field(min_length=3, max_length=50, examples=['dfhaskdf&^R&^*B^w98723'])
    age: str = Field(min_length=1, max_length=2, examples=['14'])
    ip: str = Field(min_length=1, max_length=50, examples=['198.0.31.4'])
    city: str = Field()
    country: str = Field()
    region: str = Field()




class AuthRegistered(BaseModel):
    success: bool = Field(examples=[True])
    id: int = Field(examples=[656])
    login: EmailStr = Field(examples=['login@ukr.net'])



class AuthLogin(BaseModel):
    login: EmailStr = Field(examples=['login@ukr.net'])
    password: str = Field(min_length=settings.Settings.MIN_PASSWORD_LENGTH, max_length=50, examples=['dfhaskdf&^R&^*B^w98723'])
   
