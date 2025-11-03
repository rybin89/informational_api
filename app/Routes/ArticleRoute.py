import peewee
from flask import Blueprint, Flask, jsonify, request

from app.Contollers.ArticleController import ArticleController
from app.Contollers.TokenController import TokenController

article_bp = Blueprint('articles', __name__, url_prefix='/api/articles')


@article_bp.route('/', methods=['GET'])
def get():
    articles = ArticleController.get()
    # серилизовать полученный список обектов articles в json
    list = []
    for article in articles:
        list.append(
            {
                'id': article.id,
                'title': article.title,
                'slug': article.slug,
                'excerpt': article.excerpt,
                'content': article.content,
                'featured_image': article.featured_image,
                'status': article.status,
                'views': article.views,
                'reading_time': article.reading_time,
                'author': article.author.username,
                'category': article.category.name,
                'published_at': article.published_at,
                'created_at': article.created_at,
                'updated_at': article.updated_at,

            }
        )
    return jsonify(
        {
            'access': True,
            'articles': list
        }
    ), 200
@article_bp.route('/<slug>', methods=['GET'])
def get_by_slug(slug):
    article = ArticleController.show_slug(slug)
    return jsonify(
        {
            'success': True,
            'article': {
                'id': article.id,
                'title': article.title,
                'slug': article.slug,
                'excerpt': article.excerpt,
                'content': article.content,
                'featured_image': article.featured_image,
                'status': article.status,
                'views': article.views,
                'reading_time': article.reading_time,
                'author': article.author.username,
                'category': article.category.name,
                'published_at': article.published_at,
                'created_at': article.created_at,
                'updated_at': article.updated_at,
            }
        }

    ),200
@article_bp.route('/', methods=['POST'])
@TokenController.requeired
@TokenController.role_requeired('author')
def add(user,token):
    print(user)
    data_article = request.get_json()
    if data_article is None:
        return jsonify(
            {
                'success': False,
                'message': 'Данные о статье отстутсвуют'
            }
        ), 400
    title = data_article['title']
    content = data_article['content']
    category = data_article['category']
    article = ArticleController.add(
            title=title,
            content=content,
            author=user['user_id'],
            category=category
    )

    return jsonify(
        {
            'success': True,
            'message' : 'Статья создана',
            'article': {
                'id': article.id,
                'title': article.title,
                'slug': article.slug,
                'excerpt': article.excerpt,
                'content': article.content,
                'featured_image': article.featured_image,
                'status': article.status,
                'views': article.views,
                'reading_time': article.reading_time,
                'author': article.author.username,
                'category': article.category.name,
                'published_at': article.published_at,
                'created_at': article.created_at,
                'updated_at': article.updated_at,
            }
        }

    ), 200
@article_bp.route('/',methods=['PUT'])
@TokenController.requeired
@TokenController.role_requeired('author')
def update(user,token):
    pass


