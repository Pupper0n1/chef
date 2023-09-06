from ninja import Schema, ModelSchema
from .models import Profile

class ProfileSchema(ModelSchema):
    class Config:
        model = Profile
        model_fields = ['id', 'bio', 'picture', 'friends', 'followers']


class NotFoundSchema(Schema):
    message: str


class ProfileIn(Schema):
    username: str
    password: str

