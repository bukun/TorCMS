from .models import myuser, admingroup
from rest_framework import generics
from rest_framework import permissions
from .serializers import UsersSerializer, GroupSerializer,myuserregisterserializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django_filters import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserProfileForm
from friendship.models import Block, Follow, Friend, FriendshipRequest
from .forms import LoginForm,RegisterForm
User = get_user_model()


class UserList(generics.ListCreateAPIView):
    queryset = myuser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # 经过身份验证的请求获得读写访问权限，未经身份验证的请求将获得只读读的权限。

    # 仅限已经通过身份验证的用户访问；
    # permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['username', 'mobile', 'belong_jyztzz']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 用户修改个人信息，和查看用户信息，就只自己登录了，只能查看自己的信息就行
# IsOwnerOrReadOnly 还是得整个用户自定义权限，只能自己查询自己的信息，自己修改自己的信息，别被人攻击接口
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = myuser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)

    #     仅限已经通过身份验证的用户访问

    def perform_create(self, serializer):

        print('------self.request---------')
        print(self.request)
        print('------self.request.data---------')
        print(self.request.data)


class GroupList(generics.ListCreateAPIView):
    queryset = admingroup.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ['name', 'type']

    # 将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def recurse_display(data):
    """递归展示"""
    display_list = []
    for item in data:

        display_list.append(item)
        children = item.children.all()
        if len(children) > 0:
            display_list.append(recurse_display(children))
    return display_list


def grouplist(request):
    # 核心是filter(parent=None) 查到最顶层的那个parent节点
    #
    # departs = admingroup.objects.filter(parent=None)
    # data = recurse_display(departs)
    # return render(request, 'group_list.html', {'data': data})
    return render(request, 'group_list.html', {'genres': admingroup.objects.all()})


@permission_classes((AllowAny,))
class RegisterAPIveiw(APIView):
    """
    注册
    """

    def post(self, request):
        # 获取用户输入的用户名。
        username = request.data.get('username')
        # 获取用户的密码
        password1 = request.data.get('password')
        mobile = request.data.get('mobile')
        location = request.data.get('location')
        detailed_address = request.data.get('detailed_address')
        groups = request.data.get('groups[]')
        logo = request.data.get('logo')

        user = User.objects.filter(username=username)
        if user.all().count()!=0:
            return Response({'msg': '该用户名存在了', 'code': 404})
        else:

            group_list = [groups]
            user_dict = {
                'username': username,
                'password': make_password(password1),
                'mobile': mobile,
                'location': location,
                'detailed_address': detailed_address,
                'groups': group_list,
                'avatar_img': logo,
            }

            user_serializer = myuserregisterserializer(data=user_dict)
            # 进行数据校验，保存
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'msg': '注册成功', 'code': 200})
            else:
                return Response({'msg': user_serializer.errors, 'code': 400})



@permission_classes((IsAuthenticated,))
class UpdateUserAPIveiw(APIView):
    """
    用户修改信息
    """

    def put(self, request):
        # 获取用户输入的用户名。
        user = request.user
        username = request.data.get('username')

        mobile = request.data.get('mobile')
        location = request.data.get('location')
        detailed_address = request.data.get('detailed_address')
        groups = request.data.get('groups')
        avatar_img = request.data.get('avatar_img')


        if mobile!=None:
            user.mobile=mobile
        if location!=None:
            user.location=location
        if username!=None:
            user.username=username
        if detailed_address!=None:
            user.detailed_address=detailed_address
        if avatar_img!=None:
            user.avatar_img=avatar_img


        if not user.groups.filter(id=groups).exists():
            groups_new_role = admingroup.objects.get(id=groups)
            for i in ['农户','专家']:
                if i!=groups_new_role.name:
                    groups_old_role = admingroup.objects.get(name=i)
                    user.groups.remove(groups_old_role)

            user.groups.add(groups_new_role)


        try:
            user.save()
            return Response({'message': '用户信息已成功更新'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        # group_list = [groups]
        # user_dict = {
        #     'username': username,
        #     'mobile': mobile,
        #     'location': location,
        #     'detailed_address': detailed_address,
        #     'groups': group_list,
        #     'avatar_img': logo,
        # }
        #
        # user_serializer = myuserregisterserializer(data=user_dict)
        # # 进行数据校验，保存
        # if user_serializer.is_valid():
        #     user_serializer.save()
        #     return Response({'msg': '注册成功', 'code': 200})
        # else:
        #     return Response({'msg': user_serializer.errors, 'code': 400})



@permission_classes((IsAuthenticated,))
class GetUserInfo(APIView):

    def get(self, request):
        user = request.user  # 获取用户了



        if user:
            user_serializer = UsersSerializer(user)

            permissions_Set = user.get_all_permissions()  # 得到用户所有权限，结果是一个set（元组）,不能被分页
            # todo 用户所属权限组，筛选一下，只返回属于‘前台用户’的权限，其他空间权限什么的都不返回
            permissions_List = list(permissions_Set)
            return Response({
                'user_info': user_serializer.data,
                'permissions_List': permissions_List,
                'code': 200
            })
        else:
            return Response({'msg': '', 'code': 400})



# 修改密码
@permission_classes((IsAuthenticated,))
class change_user_password(APIView):


    def put(self,request):
        user = request.user

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'msg': '原密码错误', 'code': 400})
        user.set_password(new_password)
        user.save()
        return Response({'msg': '修改成功', 'code': 200})


@login_required(login_url='users:login')
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/users/profile/')  # Redirect to a success page.
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required(login_url='users:login')
def user_profile(request):
    username = request.user.username
    email = request.user.email
    # 获取当前用户的所有朋友
    all_friends = Friend.objects.friends(request.user)

    # 获取所有未读的友谊请求
    requests = Friend.objects.unread_requests(user=request.user)

    # 获取所有关注当前用户的人
    followers = Follow.objects.followers(request.user)

    # 获取当前用户关注的所有人
    following = Follow.objects.following(request.user)

    # List of this user's friends
    all_friends = Friend.objects.friends(request.user)

    # List all unread friendship requests
    requests = Friend.objects.unread_requests(user=request.user)

    # List all rejected friendship requests
    rejects = Friend.objects.rejected_requests(user=request.user)

    # # List of this user's followers
    # all_followers = Following.objects.followers(request.user)
    #
    # # List of who this user is following
    # following = Following.objects.following(request.user)

    ### Managing friendship relationships
    # other_user = User.objects.get(pk=1)
    # new_relationship = Friend.objects.add_friend(request.user, other_user)
    # Friend.objects.are_friends(request.user, other_user) == True
    # Friend.objects.remove_friend(other_user, request.user)
    #
    # # Can optionally save a message when creating friend requests
    # some_other_user = User.objects.get(pk=2)
    # message_relationship = Friend.objects.add_friend(
    #     from_user=request.user,
    #     to_user=some_other_user,
    #     message='Hi, I would like to be your friend',
    # )
    #
    # # Attempting to create an already existing friendship will raise
    # # `friendship.exceptions.AlreadyExistsError`, a subclass of
    # # `django.db.IntegrityError`.
    # dupe_relationship = Friend.objects.add_friend(request.user, other_user)
    # AlreadyExistsError: u'Friendship already requested'
    #
    # # Create request.user follows other_user relationship
    # following_created = Following.objects.add_follower(request.user, other_user)
    #
    # # Attempting to add an already existing follower will also raise
    # # `friendship.exceptions.AlreadyExistsError`,
    # dupe_following = Following.objects.add_follower(request.user, other_user)
    # AlreadyExistsError: u"User 'alice' already follows 'bob'"
    #
    # was_following = Following.objects.remove_follower(request.user, other_user)
    #
    # # Create request.user blocks other_user relationship
    # block_created = Block.objects.add_block(request.user, other_user)
    #
    # # Remove request.user blocks other_user relationship
    # block_remove = Block.objects.remove_block(request.user, other_user)

    # from django.contrib.auth.models import User
    # from friendship.models import  Follow,Request
    #
    # # 关注者和被关注者关系
    # follower_following = Follow.objects.create(from_user=User, to_user=User)
    #
    # # 请求关注（如果被关注者接受了请求，关系就创建了）
    # request = Request.objects.create(from_user=User, to_user=User)
    #
    # # 获取关注者和被关注者的列表
    # followers = Follow.objects.followers(user=User)
    # following = Follow.objects.following(user=User)
    #
    # # 检查关系状态
    # status = Follow.objects.get_status(from_user=User, to_user=User)

    # 如果你想要更复杂的查询，可以使用自定义的模型管理器

    # 查询当前用户可以添加的好友
    #
    # potential_friends = myuser.objects.exclude(
    #     id=request.user.id
    # ).exclude(
    #     friend__to=request.user,
    #     friend__from=request.user,
    #     friend__status='accepted'
    # )

    return render(request, 'users/profile.html', {'username': username, 'email': email, 'all_friends': all_friends,
                                                  'requests': requests,
                                                  'followers': followers,
                                                  'following': following,})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/users/profile/')
            else:
                error_message = '用户名或密码错误，请重试。'
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)  # 使用Django的logout函数来注销用户
    return HttpResponseRedirect(reverse('users:login'))  # 重定向到登录页面，这里的'login_url'是登录页面的名称


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')  # 假设有登录页面
    template_name = 'users/register.html'
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/login/')   # 假设有一个登录视图名为'login'

    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})