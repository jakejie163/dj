# -*- coding:UTF-8 -*-

from rest_framework import serializers

from profiles.serializers import ProfileSerializer

from .models import Article, Comment, Tag
from .relations import TagRelatedField

class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    tagList = TagRelatedField(many=True, required=False, source='tags')
    slug = serializers.SlugField(required=False)
    description = serializers.CharField(required=False)
    
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at') 

    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count'
    )

    class Meta:
        model = Article
        fields = (
            'author',
            'tagList',
            'title',        # one
            'slug',
            'description',  # 自定义非必须，后端数据模型保持数据完整性
            'body',         # two

            'createdAt',
            'updatedAt',

            'favorited',
            'favoritesCount',
        )

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
    
    def get_favorited(self, instance):
        request = self.context.get('request', None)  # 从这里处理接收的上下文
        
        if request is None:
            return False

        if not request.user.is_authenticated():
            return False

        return request.user.profile.has_favorited(instance) # 用户是否喜欢了这个实例

    def get_favorites_count(self, instance):
        return instance.favorited_by.count()
    

    def create(self, validated_data):
        author = self.context.get('author', None)  #可以不通过外部接收
        tags = validated_data.pop('tags', [])

        article = Article.objects.create(author=author, **validated_data)

        for tag in tags:
            article.tags.add(tag)

        return Article


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at') 

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'body',         # 其实输入只要传递一个body就的了
            'createdAt',
            'updatedAt',
        )

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

    def create(self, validated_data):
        article = self.context['article']  # 通过视图上下文传递
        author = self.context['author']

        return Comment.objects.create(
            author=author, article=article, **validated_data
        )
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)

        def to_representation(self, obj):
            return obj.tag
