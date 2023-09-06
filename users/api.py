from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate
from .models import Profile, User
from django.contrib.auth import authenticate, login, logout
from .schema import ProfileSchema, NotFoundSchema, ProfileIn
from django.contrib.auth.decorators import login_required


router = Router()


@router.get('/', response={200: list[ProfileSchema], 404: NotFoundSchema})
def list_profiles(request, username: str = None):
    if username:
        return Profile.objects.filter(user__username__icontains=username)
    return Profile.objects.all()


@router.get('/{int:id}', response={200: ProfileSchema, 404: NotFoundSchema})
def get_profile(request, id: int):
    try:
        return 200, Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        raise HttpError(404, f"Profile with id {id} not found")


@router.post('/create_user', response={201: ProfileSchema})
def create_user(request, username: str, password: str, email: str):
    if User.objects.filter(username=username).exists():
        raise HttpError(400, "Username already exists!")
    user = User(username=username, email=email)
    user.set_password(password) # Hashes the password and saves
    user.save()
    return 201, Profile.objects.create(user=user, bio="", picture="")


@router.post('/login', response={200: ProfileSchema, 404: NotFoundSchema})
def profile_login(request, profile: ProfileIn):
    user = authenticate(request, username=profile.username, password=profile.password)
    if user is not None:
        login(request, user)
        return Profile.objects.get(user=user)
    else:
        raise HttpError(400, "Invalid credentials!")


@router.post('/logout', response={200: str})
def profile_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return 200, "Successfully logged out"
    else:
        "Already logged out!"


