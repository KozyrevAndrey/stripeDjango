# stripeDjango
One-page site for stripe API. Stripe - payment system. 

Для стабильный работы необходим Django~=3.2.10 версии и stripe~=5.0
Однако, можно использовать и более свежие версии django. Все зависит от вашего сервера.

Используем виртуальное окружение и устанавливаем django и stripe. 

pip install django==3.2.10

pip install stripe

Первоначальные настройки и команды:
1. py django-admin startproject stripeDjango
2. py manage.py migrate
3. py manage.py createsuperuser
4. Создаем папку templates в корневой папке проекта;
5. Добавляем в settings:
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        ...
    },
]

Для продолжения работы и налаживания связи с stripe API необходимо зарегистрироваться. 
Регистрируемся, получаем stripe_public_key и stripe_secret_key. Создаем продукты, которые будут работать с stripe API. 
У продуктов будет name, description, price, product_id и product_price_id. 
Передавая данные в stripe, будет происходить создание сессии оплаты на стороне API.
Они нужны для взаимодействия и для использования в django models.

Создаем model in models.py, и запускаем makemigration и migrate:

from django.db import models

from django.urls import reverse
class Item(models.Model):
    name = models.CharField(max_length=100) # Название продукта
    description = models.CharField(max_length=400) # Описание продукта 
    price = models.IntegerField(default=0) # Цена продукта
    stripe_product_id = models.CharField(max_length=100) 
    stripe_price_id = models.CharField(max_length=100)

    def __str__(self): # функция для отображения в админ панеле 
        return self.name

    def get_display_price(self): # функция для отображение цены, если используются центы 
        return "{0:.2f}".format(self.price)

    def get_absolute_url(self): # функция для создания ссылки перехода на детали продукта
        return reverse('detail', args=[str(self.id)])
        
 Далее необходимо ввести в админ панель данные Item. Должны быть такими же, как и в stripe. 
 Вводим данные. Теперь данные можно использовать в views и templates.
 
 Необходимо внести в settings данные ключей stripe. 
 Вносим:

 STRIPE_PUBLIC_KEY = "pk_test_1234"
 STRIPE_SECRET_KEY = "sk_test_1234"
 
 Следущим шагом будет создание stripe.checkout.Session.create. 
 Создаем класс для checkoutsession. Он будет использоваться при переходе на оплату.
 class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"]) # обращаемся к primarykey
        domain = "https://yourdomain.com"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)
        
     
Создадим SuccessView и CancelView и templates для них. Если операция успешна - переходим на success_url, если нет, то на cancel_url.
class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"
    
    
Создадим представления для главной страницы, где будут все продукты, и заодно создадим представление для подробностей продуктов

class ProductLandingPageView(TemplateView):
    template_name = 'landing.html'
    
    def get_context_data(self, **kwargs): # Функция для получения объектов из models
        product = Item.objects.all()
        context = super(ProductLandingPageView,
                        self).get_context_data(**kwargs)
        context.update({
            'product': product,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIС_KEY, # public_key для redirect_session
        })
        return context


class ArticleDetailView(DetailView):
    model = Item
    template_name = 'detail.html'

    def get_product(self):
        product = Item.objects.all()
        context = super(ArticleDetailView,
                        self).get_context_data()
        context.update({
            'product': product,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIС_KEY
        })
        return context



Сейчас прописываем все urls. 
urlpatterns = [
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('buy/<pk>/', CreateCheckoutSession.as_view(), name='buy'),
    path('', ProductLandingPageView.as_view(), name='landing'),
    path('item/<pk>/', ArticleDetailView.as_view(), name='detail')
]


Можно тестировать и проверять работу!










