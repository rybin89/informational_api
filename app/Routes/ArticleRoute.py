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
    try:

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
    except peewee.IntegrityError as error:
        return jsonify(
            {
                'success': False,
                'message': 'Статья не создана',
                'error': str(error)
            }
        ),400
@article_bp.route('/<int:id>',methods=['PUT'])
@TokenController.requeired
def update(id,user,token):
    # Статья пренадлежит этому автору
    atricle = ArticleController.show(id)
    if atricle is None:
        return jsonify(
            {
                'success': False,
                'message': 'Не найдено',

            }
        ), 404
    if atricle.author.id != user['user_id']:
        return jsonify(
            {
                'success': False,
                'message': 'Запрещено',

            }
        ),403
    try:
        if not request.is_json:
            return jsonify(
                {
                    "success": False,
                    "error": "Нет данных"
                }
            ), 422
        article_data = request.get_json()
        if article_data is None:
            return jsonify(
                {
                    "success": False,
                    "error": "Нет данных"
                }
            ), 422

        ArticleController.update(id, **article_data)
        article_new = ArticleController.show(id)

        return jsonify(
            {
                "success": True,
                "message": f"Категория {atricle.title} измениена",
                'article': {
                    'id': article_new.id,
                    'title': article_new.title,
                    'slug': article_new.slug,
                    'excerpt': article_new.excerpt,
                    'content': article_new.content,
                    'featured_image': article_new.featured_image,
                    'status': article_new.status,
                    'views': article_new.views,
                    'reading_time': article_new.reading_time,
                    'author': article_new.author.username,
                    'category': article_new.category.name,
                    'published_at': article_new.published_at,
                    'created_at': article_new.created_at,
                    'updated_at': article_new.updated_at,
                }

            }
        ), 201
    except TypeError as error:
        return jsonify(
            {
                "success": False,
                "error": f"{error}"
            }
        ), 500
    except peewee.IntegrityError as error:
        return jsonify(
            {
                "success": False,
                "error": f"{error}"
            }
        ), 422

@article_bp.route('/<int:id>',methods=['DELETE'])
@TokenController.requeired
def delete(id,user,token):
    article = ArticleController.show(id)
    if article is None:
        return jsonify(
            {
                'success': False,
                'message': 'Не найдено',

            }
        ), 404
    if article.author.id != user['user_id']:
        return jsonify(
            {
                'success': False,
                'message': 'Запрещено',

            }
        ), 403
    ArticleController.delete(id)
    return jsonify(
        {
            'success': True,
            'message': 'Статья удалена',
        }
        ),200



