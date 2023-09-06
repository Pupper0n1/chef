from ninja import Schema, ModelSchema
from .models import Post



class PostSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = ['author', 'title', 'description', 'image', 'likes', 'date_created', 'date_updated'] 
        # model_fields_optional = ['description', 'image', 'likes']