from django.shortcuts import render
from rest_framework import generics,mixins,status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Post, Vote, Comment
from .serializers import PostSerializer, VoteSerializer, CommentSerializer
# Create your views here.


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(post=self.request.user)

class SinglePost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    

class Voter(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post :)')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))   

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never voted for this post Bruh') 

class Comments(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]      

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk']) 
        return Comment.objects.filter(user=user, post=post)
        # return Comment.objects.filter(user=user, post=post).order_by('comment')[:1] 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post=Post.objects.get(pk=self.kwargs['pk'])) 

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never commented for this post Bruh') 

class Commentsdel(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]      

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk']) 
        # print(Comment.objects.filter(user=user, post=post, pk=self.kwargs['pk1']))
        if Comment.objects.filter(user=user, post=post, pk=self.kwargs['pk1']).exists():
            return Comment.objects.filter(user=user, post=post, pk=self.kwargs['pk1'])
        else:
            raise ValidationError('No comment for this iD') 

        # return Comment.objects.filter(user=user, post=post).order_by('comment')[:1] 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post=Post.objects.get(pk=self.kwargs['pk'])) 

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never commented for this post Bruh')             