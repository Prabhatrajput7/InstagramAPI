from rest_framework import serializers
from .models import Post, Vote, Comment

class PostSerializer(serializers.ModelSerializer):

    post = serializers.ReadOnlyField(source='post.username')
    votes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','title','url','post','votes','con','comments']

    def get_votes(self, post):
        """
        print('POST'+str(post))
        print('VOte'+str(Vote.objects.filter(post=post)))
        Maching id here post=post
        """
        return Vote.objects.filter(post=post).count()

    def get_comments(self, post):
        l = []
        # print(Comment.objects.filter(post=post))
        # return Comment.objects.filter(post=post).count()
        for i in Comment.objects.filter(post=post):
            l.append(i.comment)
        return l

class CommentSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = ['id','comment','user','post']        

class VoteSerializer(serializers.ModelSerializer):

    voter = serializers.ReadOnlyField(source='voter.username')
    post = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Vote
        fields = ['voter','post']


    
