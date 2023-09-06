from ninja import Router
from ninja.orm import create_schema
from ninja.errors import HttpError
from ninja.pagination import paginate
from .models import Post
from .schema import PostSchema
from typing import List

router = Router()


@router.get("/", response={200: List[PostSchema]})
def list_posts(request, title: str = None, author: str = None):
    if title:
        posts = Post.objects.filter(title__icontains=title)
    elif author:
        posts = Post.objects.filter(author__icontains=author)
    else:
        posts = Post.objects.all()
    
    if not posts.exists():
        raise HttpError(404, "No posts found!")
    
    return 200, posts


@router.get("/{int:user_id}", response={200: List[PostSchema]})
def get_user_posts(request, user_id: int):
    posts = Post.objects.filter(author__id=user_id)
    print(posts.values('date_updated'))
    return 200, posts


@router.post('/create', response={200: PostSchema})
def create_post(request, post_data: PostSchema):
    post = post_data.dict()
    return Post.objects.create(**post)



@router.delete('/delete/{int:post_id}', response={200: str})
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise HttpError(404, "Post does not exist!")
    post.delete()
    return 200, "Post deleted!"



