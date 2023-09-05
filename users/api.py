from ninja import Router, Schema
from ninja.errors import HttpError
from .models import Profile, User
from django.contrib.auth import authenticate, login

router = Router()

class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str = None
    last_name: str = None

class ProfileSchema(Schema):
    id: int
    bio: str = None
    picture: str = None
    user: UserSchema
    friends: list[str]
    followers: list[str]

class NotFoundSchema(Schema):
    message: str


@router.get('/', response={200: list[ProfileSchema], 404: NotFoundSchema})
def list_profiles(request, username: str = None):
    if username:
        return Profile.objects.filter(user__username__icontains=username)
    # return Profile.objects.all()
    print(Profile.objects.all())
    return Profile.objects.all()
    # return profiles.values('id', 'bio', 'picture', 'user__username', 'friends__user__username', 'followers__user__username')


@router.get('/{id}', response={200: ProfileSchema, 404: NotFoundSchema})
def get_profile(request, id: int):
    try:
        return 200, Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        raise HttpError(404, f"Profile with id {id} not found")


@router.post('/create_user', response={200: ProfileSchema})
def create_user(request, username: str, password: str, email: str):

    if User.objects.filter(username=username).exists():
        raise HttpError(400, "Username already exists!")

    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    profile = Profile(user=user, bio="", picture="")
    print(profile)
    profile.save()
    return 201, profile



@router.post('/login', response={200: ProfileSchema, 404: NotFoundSchema})
def login(request, username: str, password: str):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Profile.objects.get(user=user)
    else:
        raise HttpError(400, "Invalid credentials!")
        

# @router.post()