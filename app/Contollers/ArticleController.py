from app.Models.Article import Article
from transliterate import  translit

class ArticleController:

    @classmethod
    def add(cls,title, content, author, category=None, status='draft'):
        slug = translit(title, 'ru', reversed=True)
        slug = slug.lower().replace(' ', '_')

        Article.create(
            title=title,
            content=content,
            slug=slug,
            author=author,
            category=category,
            status=status
        )
        return cls.show_slug(slug)

    @classmethod
    def get(cls):
        return Article.select()

    @classmethod
    def show_slug(cls, slug):
        return Article.get_or_none(slug=slug)

    @classmethod
    def show_category(cls, category_id):
        return Article.select().where(Article.category == category_id)
    @classmethod
    def show(cls,id):
        return Article.get_or_none(id)

    @classmethod
    def update(cls,id,**filds):
        Article.update(**filds).where(Article.id == id).execute()
    @classmethod
    def delete(cls,id):
        Article.delete_by_id(id)
if __name__ == '__main__':

   #  str = '''
   # Согласно российскому законодательству программой для ЭВМ является представленная в объективной форме совокупность данных и команд, предназначенных для функционирования ЭВМ и других компьютерных устройств в целях получения определенного результата, включая подготовительные материалы, полученные в ходе разработки программы для ЭВМ, и порождаемые ею аудиовизуальные отображени
   # '''
   #  ArticleController.add(
   #      title='Программное обеспечение',
   #      content=str,
   #      author=20,
   #      category=1
   #
   #  )
   print(ArticleController.show(2).author.id)