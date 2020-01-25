from django.shortcuts import render
from .models import Post
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from .forms import SignUpForm
from .forms import BlogForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.shortcuts import redirect, reverse
from rest_framework.views import  APIView
from .serializers import PostSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from rest_framework.generics import ListAPIView
from .serializers import PostDetailSerializer
from .models import Comment



# Create your views here.

# class PostList(APIView):
#     serializer_class = PostSerializer
#
#     # def get(self, request, format=None):
#     #     objects = PostSerializer(Post.objects.filter(status=1).order_by('-created_on'), many=True)
#     #     self.meta_data = "GET"
#     #     self.module = "Member"
#     #     self.data = objects.data
#     #     if objects is None:
#     #         self.error = "datas are not found"
#     #         return Response(self.response_obj, status=status.HTTP_404_NOT_FOUND)
#     #     else:
#     #         return Response(self.response_obj, status=status.HTTP_200_OK)
#     #     pass
#
#
#     def get(self, request, format= None):
#         queryset = Post.objects.filter(status=1).order_by('-created_on')
#         serializer = PostSerializer(queryset, many = True)
#         paginate_by = 10
#         return Response(serializer.data)



# @api_view(['POST'])
# def create_blog(request):
#     #form = PostSerializer()
#     #context = {'form':form}
#     #new_post = None
#     if request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         #print(request.data)
#         if serializer.is_valid(raise_exception = True):
#             user = User.objects.first()
#             serializer.save(author=user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 10


def create_blog(request):
    form = BlogForm()
    context = {'form':form}
    new_post = None
    if request.method == 'POST':

        form = BlogForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:home')

    return render(request,'registration/create.html',context)



# @api_view(['GET','POST'])
def post_detail(request, id):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, pk=id)

    #elif request.method == 'POST':

    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.active = True
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def draft_detail(request,id):
    template_name = 'draft_detail.html'
    post = get_object_or_404(Post,pk=id)
    form = BlogForm(instance=post)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:home')
    context = {'form': form}
    return render(request,template_name,context)






