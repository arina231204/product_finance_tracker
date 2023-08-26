from _decimal import Decimal

from django.core.validators import MaxValueValidator
from django.db import models, transaction

from django.db import models

from accounting.models import Purchase, Expenses, Balance

is_included_in_tax_report_choices = [
    ('1', 'Совпадает с группой'),
    ('2', 'ОСН'),
    ('3', 'УСН. Доход'),
    ('4', 'УСН. Доход-Расход'),
    ('5', 'ЕСХН'),
    ('6', 'ЕНВД'),
    ('7', 'Патент'),
]

status_choices = [
    ('1', 'Новый'),
    ('2', 'Выслано предложение'),
    ('3', 'Переговоры'),
    ('4', 'Сделка заключена'),
    ('5', 'Сделка не заключена'),
]

contractor_type_choices = [
    ('1', 'Юридическое лицо'),
    ('2', 'Индивидуальный предприниматель'),
    ('3', 'Физическое лицо'),
]
PRICE_CHOICES = [
    ('1', 'Цена продажи'),
]
balance_type_choices = [
    ('1', 'В сумме на всех складах'),
    ('2', 'Одинаковый на всех складах'),
    ('3', 'Задать для каждого склада'),
]
PACKAGING_TYPES = [
    ('1', 'Фасовка'),
    ('2', 'Штучная'),
    ('3', 'Разливная '),
]

ACCOUNTING_TYPE_CHOICES = [
    ('1', 'Без специализированного учета'),
    ('2', 'Алкогольный товар'),
    ('3', 'Учет по серийным номерам '),
    ('4', 'Средство индивидуальной защиты'),

]
production_type_choices = [
    ('1', 'Произведен в КР'),
    ('2', 'Ввезен в КР'),
]
product_type_choices = [
    ('1', 'Не маркируется'),
    ('2', 'Обувь'),
    ('3', 'Одежда'),
    ('4', 'Постельное белье'),
    ('5', 'Духи и туалетная вода'),
    ('6', 'Фотокамеры и лампы-вспышки'),
    ('7', 'Шины и покрышки'),
    ('8', 'Молочная продукция'),
    ('9', 'Упакованная вода'),
    ('10', 'Альтернативная табачная продукция'),
    ('11', 'Никотиносодержащая продукция'),
    ('12', 'Табачная продукция'),
]

GENDER_CHOICES = (
    ('1', 'Унисекс'),
    ('2', 'Мужской'),
    ('3', 'Женский'),
    ('4', 'Детский'),
)
PAYMENT_CHOICES = [
    ('1', 'Совпадает с точкой'),
    ('2', 'Подакцизный товар'),
    ('3', 'Товар'),
    ('4', 'Подакцизный товар'),
    ('5', 'Составной предмет расчета'),
    ('6', 'Иной предмет расчета'),
]


class Country(models.Model):
    name = models.CharField(verbose_name='Страна', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страна'


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование группы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class NDS(models.Model):
    rate = models.PositiveSmallIntegerField(verbose_name='Ставка НДС', validators=[MaxValueValidator(99)])
    comment = models.CharField(max_length=32, verbose_name='Комментарий', blank=True, null=True)
    user = models.CharField(max_length=32, verbose_name='Пользователь', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отдел')

    def __str__(self):
        return f'{self.rate}%'

    class Meta:
        verbose_name = 'НДС'
        verbose_name_plural = 'НДС'


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование группы')
    description = models.TextField(blank=True, verbose_name='Описание')
    parent_group = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='Родительская группа')
    code = models.CharField(max_length=255, verbose_name='Код')
    external_code = models.CharField(max_length=255, verbose_name='Внешний код')
    vat_enabled = models.ForeignKey(NDS, on_delete=models.CASCADE, verbose_name='НДС')
    is_included_in_tax_report = models.CharField(verbose_name='Система налогообложения', max_length=10,
                                                 choices=is_included_in_tax_report_choices, default='1', )
    employee = models.CharField(max_length=255, verbose_name='Сотрудник')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отдел')
    is_shared = models.BooleanField(default=False, verbose_name='Общий доступ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Warehouse(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    address_comment = models.TextField(blank=True, verbose_name='Комментарий к адресу')
    code = models.CharField(max_length=20, verbose_name='Код')
    groups = models.ManyToManyField('Group', blank=True, verbose_name='Группы')
    external_code = models.CharField(max_length=50, blank=True, verbose_name='Внешний код')
    employee = models.CharField(max_length=100, verbose_name='Ответственный сотрудник')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='Отдел')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    code = models.CharField(max_length=20, verbose_name='Код')
    description = models.TextField(blank=True, verbose_name='Описание')
    employee = models.CharField(max_length=100, verbose_name='Сотрудник')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отдел')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name


class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'


class BankCode(models.Model):
    bic = models.CharField(max_length=9, verbose_name='БИК')
    bank_name = models.CharField(max_length=255, verbose_name='Банк')
    address = models.TextField(verbose_name='Адрес')
    correspondent_account = models.CharField(max_length=20, verbose_name='Корр. счет')
    checking_account = models.CharField(max_length=20, verbose_name='Расчетный счет')

    def __str__(self):
        return self.bank_name

    class Meta:
        verbose_name_plural = 'Расчетные коды'


class Contractor(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=255)
    description = models.TextField(verbose_name='Описание', blank=True)
    status = models.CharField(verbose_name='Статус', max_length=20, choices=status_choices)
    groups = models.ManyToManyField(Group, verbose_name='Группы', blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20, blank=True)
    fax = models.CharField(verbose_name='Факс', max_length=20, blank=True)
    email = models.EmailField(verbose_name='Электронный адрес', blank=True)
    address = models.CharField(verbose_name='Фактический адрес', max_length=255, blank=True)
    address_comment = models.TextField(verbose_name='Комментарий к адресу', blank=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    code = models.CharField(verbose_name='Код', max_length=20, blank=True)
    external_code = models.CharField(verbose_name='Внешний код', max_length=20, blank=True)
    contacts = models.ManyToManyField(Contact, verbose_name='Контактные лица', blank=True)
    contractor_type = models.CharField(verbose_name='Тип контрагента', max_length=100, choices=contractor_type_choices,
                                       blank=True)
    inn = models.CharField(verbose_name='ИНН', max_length=14, blank=True)
    legal_entity_name = models.CharField(verbose_name='Полное наименование', max_length=255, blank=True)
    legal_entity_address = models.CharField(verbose_name='Юридический адрес', max_length=255, blank=True)
    legal_entity_address_comment = models.TextField(verbose_name='Комментарий к адресу', blank=True)
    # inn_fill_by_inn = models.BooleanField(verbose_name='Заполнить по ИНН', default=False)
    kpp = models.CharField(verbose_name='КПП', max_length=9, blank=True)
    ogrn = models.CharField(verbose_name='ОГРН', max_length=15, blank=True)
    okpo = models.CharField(verbose_name='ОКПО', max_length=10, blank=True)
    bank_accounts = models.ManyToManyField(BankCode, verbose_name='Расчетный счет', blank=True)
    price_type = models.CharField(max_length=50, choices=PRICE_CHOICES, default='1', verbose_name='Цены')
    discount_card_number = models.CharField(verbose_name='Номер дисконтной карты', max_length=50)

    access_choices = [
        ('full', 'Полный'),
        ('partial', 'Ограниченный'),
        ('none', 'Нет доступа'),
    ]
    employee = models.CharField(max_length=50, verbose_name='Сотрудник')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отдел')
    shared_access = models.BooleanField(verbose_name='Общий доступ', default=False)

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class UnitOfMeasurement(models.Model):
    short_name = models.CharField(verbose_name='Краткое наименование', max_length=20)
    full_name = models.CharField(verbose_name='Полное наименование', max_length=255)
    code = models.PositiveSmallIntegerField(verbose_name='Цифровой код', unique=True)

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.short_name


class EGAISCode(models.Model):
    code = models.CharField(max_length=20, verbose_name='Код ЕГАИС')

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'Код ЕГАИС'
        verbose_name_plural = 'Коды ЕГАИС'


class AccountingFeatures(models.Model):
    packaging_type = models.CharField(verbose_name='Тип учета фасовки', choices=PACKAGING_TYPES, max_length=100)
    accounting_type = models.CharField(verbose_name='Тип учета', choices=ACCOUNTING_TYPE_CHOICES, max_length=100)
    product_code = models.CharField(verbose_name='Код вида продукции', max_length=255)
    tare_capacity = models.IntegerField(verbose_name='Емкость тары, л.')
    strength = models.DecimalField(verbose_name='Крепость', max_digits=5, decimal_places=2)
    name = models.CharField(verbose_name='Наименование', max_length=255)
    product_type = models.CharField(verbose_name='Тип продукции', max_length=255, choices=product_type_choices)
    tnved = models.CharField(verbose_name='ТН ВЭД', max_length=255)
    gender = models.CharField(verbose_name='Целевой пол', max_length=100, choices=GENDER_CHOICES)
    production_type = models.CharField(verbose_name='Тип производства', max_length=255, choices=production_type_choices)
    traceable = models.BooleanField(verbose_name='Прослеживаемый')
    kit = models.BooleanField(verbose_name='Комплект')
    egais_code = models.ForeignKey(EGAISCode, on_delete=models.CASCADE, verbose_name='Код ЕГАИС', null=True, blank=True)

    class Meta:
        verbose_name = 'Особенности учета'
        verbose_name_plural = 'Особенности учета'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Наименование товара', max_length=255)
    description = models.TextField(verbose_name='Описание')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    supplier = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name='Поставщик')
    article = models.CharField(verbose_name='Артикул', max_length=255)
    code = models.CharField(verbose_name='Код', max_length=10, unique=True, db_index=True)
    external_code = models.CharField(verbose_name='Внешний код', max_length=255)
    unit = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE, verbose_name='Единица измерения')
    weight = models.DecimalField(verbose_name='Вес', max_digits=10, decimal_places=2)
    volume = models.DecimalField(verbose_name='Объем', max_digits=10, decimal_places=2)
    vat = models.ForeignKey(NDS, on_delete=models.CASCADE, verbose_name='НДС')
    accountingFeatures = models.ForeignKey(AccountingFeatures, on_delete=models.CASCADE,
                                           verbose_name='Особенности учета')

    barcode_name = models.CharField(verbose_name='Штрихкод имя', max_length=13)
    barcode = models.CharField(verbose_name='Штрихкод', max_length=255)
    cash_receipt = models.BooleanField(verbose_name='Кассовый чек', default=False)
    tax_system = models.CharField(verbose_name='Система налогообложения', max_length=10,
                                  choices=is_included_in_tax_report_choices, default='1', )
    payment_attribute = models.CharField(verbose_name='Признак предмета расчета', max_length=255,
                                         choices=PAYMENT_CHOICES)
    employee = models.CharField(verbose_name='Сотрудник', max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Отдел')
    min_price = models.DecimalField(verbose_name='Минимальная цена', max_digits=10, decimal_places=2, default=0)
    purchase_price = models.DecimalField(verbose_name='Закупочная цена', max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(verbose_name='Цена продажи', max_digits=10, decimal_places=2, default=0)
    allow_discount = models.BooleanField(verbose_name='Запретить скидки при продаже в розницу', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'




class Receipt(models.Model):
    number = models.CharField(max_length=20, verbose_name="Номер операции")
    date = models.DateTimeField(verbose_name="Дата операции", auto_now_add=True)
    counterparty = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name="Контрагент")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    employee = models.CharField(max_length=100, verbose_name="Сотрудник")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отдел")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Склад")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Позиция")
    quantity = models.IntegerField(verbose_name="Количество")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Накладные расходы")
    file = models.FileField(upload_to='receipt_files/', blank=True, verbose_name="Файл")
    approved = models.BooleanField(default=False, verbose_name="Проведено")

    class Meta:
            verbose_name = "Оприходование"
            verbose_name_plural = "Оприходования"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            product = self.product
            price = product.purchase_price * self.quantity
            purchase, _ = Purchase.objects.get_or_create(product=product, quantity=self.quantity, price=price)
            purchase.save()
            inventory, _ = Remains.objects.get_or_create(product=product, defaults={'remaining_quantity': 0})
            inventory.remaining_quantity += self.quantity
            inventory.save()



    def __str__(self):
        return f"{self.number} - {self.date}"





class Сancellation(models.Model):
    number = models.CharField(max_length=20, verbose_name="Номер операции")
    date = models.DateTimeField(verbose_name="Дата операции", auto_now_add=True)
    counterparty = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name="Контрагент")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Проект")
    employee = models.CharField(max_length=100, verbose_name="Сотрудник")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отдел")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Склад")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Позиция")
    quantity = models.IntegerField(verbose_name="Количество")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    file = models.FileField(upload_to='receipt_files/', blank=True, verbose_name="Файл")
    approved = models.BooleanField(default=False, verbose_name="Проведено")

    class Meta:
        verbose_name = "Списание"
        verbose_name_plural = "Списания"

    def __str__(self):
        return f"{self.number} - {self.date}"



    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            product = self.product
            price = product.selling_price * self.quantity
            purchase, _ = Expenses.objects.get_or_create(product=product, quantity=self.quantity, price=price)
            purchase.save()
            inventory, created = Remains.objects.get_or_create(product=self.product)
            inventory.remaining_quantity -= self.quantity
            inventory.save()


class Inventory(models.Model):
    number = models.CharField(max_length=20, verbose_name="Номер операции")
    date = models.DateTimeField(verbose_name="Дата операции", auto_now_add=True)
    counterparty = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name="Контрагент")
    employee = models.CharField(max_length=100, verbose_name="Сотрудник")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отдел")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Склад")
    position = models.ManyToManyField(Product, verbose_name="Позиция")
    quantity = models.IntegerField(verbose_name="Количество")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    file = models.FileField(upload_to='receipt_files/', blank=True, verbose_name="Файл")

    class Meta:
        verbose_name = "Инвентаризация "
        verbose_name_plural = "Инвентаризация "

    def __str__(self):
        return f"{self.number} - {self.date}"


class Remains(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    remaining_quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} - {self.remaining_quantity}'

    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            product = self.product
            price = product.purchase_price * self.remaining_quantity
            purchase, _ = Balance.objects.get_or_create(product=product, quantity=self.remaining_quantity, price=price)
            purchase.save()

