import peewee
from flask import Blueprint, Flask, jsonify, request

from app.Contollers.CategoryController import CategoryController
from app.Contollers.TokenController import TokenController

category_bp = Blueprint('categories',__name__,url_prefix='/api/categories')

@category_bp.route('/',methods=['GET'])
def categories():
    list_categories = CategoryController.get()
    list = []
    for cat in list_categories:
        if cat.parent is None:
            parent ='Нет родителя'
        else:
            parent = cat.parent.name
        if cat.children is None:
            children = []
        else:
            children = [{'name':row.name} for row in cat.children]
        list.append({
            'id': cat.id,
            'name' : cat.name,
            'slug' : cat.slug,
            'description' : cat.description,
            'parent' : parent,
            'is_active' : cat.is_active,
            'created_at' : cat.created_at,
            'children' : children

        })
    return jsonify(list), 200
@category_bp.route('/<slug>')
def slug(slug):
    slug = CategoryController.show_slug(slug)
    if slug is None:
        return jsonify(
            {
                'success': False,
                'error' : "Нет такой категории"
             }

        ),404
    if slug.parent is None:
        parent = 'Нет родителя'
    else:
        parent = slug.parent.name
    if slug.children is None:
        children = []
    else:
        children = [{'name': row.name} for row in slug.children]
    return jsonify(
        {
            'id':slug.id,
            'name': slug.name,
            'slug': slug.slug,
            'description': slug.description,
            'parent': parent,
            'is_active': slug.is_active,
            'created_at': slug.created_at,
            'children': children
        }
    ),200

@category_bp.route('/',methods=['POST'])
@TokenController.requeired

def add_category(user,token):
    if user['role'] == 'admin' or user['role'] == 'editor':
        try:
            if not request.is_json:
                return jsonify(
                    {
                        "success": False,
                        "error": "Нет данных"
                    }
                ), 422
            category_data = request.get_json()

            if category_data is None:
                return jsonify(
                    {
                        "success": False,
                        "error": "Нет данных"
                    }
                ), 422
            name = category_data['name']
            description = category_data['description']
            parent = category_data['parent']
            if parent is None:
                parent = ''
            CategoryController.add(name,description,parent)
            return jsonify(
                {
                    "success": True,
                    "message" : f"Категория {name} добавлена"
                }
            ),201
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
@category_bp.route("/<int:id>", methods=['DELETE'])
@TokenController.requeired
@TokenController.role_requeired('admin')
def delete(id,user,token):
    try:
        category = CategoryController.show(id)
        CategoryController.delete(id)
        return jsonify(
            {
                "success": True,
                "message": f"Категория {category.name} удалена"
            }
        ), 200
    except:
        return jsonify(
            {
                "success": False,
                "error": "Ошибка"
            }
        ), 422

@category_bp.route('/<int:id>',methods=['PUT'])
@TokenController.requeired
def update(id,user,token):
    if user['role'] == 'admin' or user['role'] == 'editor':
        try:
            if not request.is_json:
                return jsonify(
                    {
                        "success": False,
                        "error": "Нет данных"
                    }
                ), 422
            category_data = request.get_json()
            if category_data is None:
                return jsonify(
                    {
                        "success": False,
                        "error": "Нет данных"
                    }
                ), 422

            CategoryController.update(id , **category_data)
            category = CategoryController.show(id)



            return jsonify(
                {
                    "success": True,
                    "message" : f"Категория {category.name} измениена",
                    'category' : {
                        'id': category.id,
                        'name': category.name,
                        'slug': category.slug,
                        'description': category.description,
                       'is_active': category.is_active,
                        'created_at': category.created_at,


                    }

                }
            ),201
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