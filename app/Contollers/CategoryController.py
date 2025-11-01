from app.Models.Category import Category
from transliterate import  translit

class CategoryController:

    @classmethod
    def get(cls):
        return Category.select()

    @classmethod
    def add(cls,name,description,parent = None):
        slug =translit(name, 'ru',reversed=True)
        slug = slug.lower().replace(' ','_')
        Category.create(name=name,slug=slug,description=description,parent=parent)

    @classmethod
    def show(cls,id):
        return Category.get_or_none(id)
    @classmethod
    def update(cls,id,**kwargs):
        for key, value in kwargs.items():
            Category.update({key: value}).where(Category.id == id).execute()
    @classmethod
    def delete(cls,id):
        Category.delete().where(Category.id == id).execute()

    @classmethod
    def show_slug(cls,slug):
        return Category.get_or_none(Category.slug == slug)
if __name__ == "__main__":
    # for row in CategoryController.get():
    #     print(row)
    #
    # CategoryController.add(
    #     'Браузерные Игры',
    #
    #     'Всё о RPG',
    #     parent=3
    # )
    # CategoryController.delete(4)
    # CategoryController.update(1,name = 'Программное обеспечение')
    for row in CategoryController.get():
        print(row.name, type(row.parent))
    print('По slug',CategoryController.show_slug('games'))

