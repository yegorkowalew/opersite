# -*- coding: utf-8 -*-
""" Модели Заказов """
from django.db import models

class Order(models.Model):
    in_id = models.IntegerField(
        verbose_name='ID',
        unique=True,
    )
    shipment_from = models.DateField(
        verbose_name='Отгрузка "от"',
        blank=True,
        null=True,
    )
    shipment_before = models.DateField(
        verbose_name='Отгрузка "до"',
        blank=True,
        null=True,
    )
    personal_no = models.CharField(
        verbose_name='П/н',
        max_length=255,
        blank=True,
        null=True,
    )
    according_to = models.CharField(
        verbose_name='Согласно КП №',
        max_length=255,
        blank=True,
        null=True,
    )
    pruduct_type = models.CharField(
        verbose_name='Тип продукции',
        max_length=255,
        blank=True,
        null=True,
    )
    product_name = models.CharField(
        verbose_name='Продукция',
        max_length=255,
        blank=True,
        null=True,
    )
    couterparty = models.CharField(
        verbose_name='Контрагент',
        max_length=255,
        blank=True,
        null=True,
    )
    order_no = models.CharField(
        verbose_name='№ Заказа',
        max_length=255,
        blank=True,
        null=True,
    )
    amount = models.FloatField(
        verbose_name='Кол-во',
        blank=True,
        null=True,
    )
    sn_no = models.CharField(
        verbose_name='№ СЗ',
        max_length=255,
        blank=True,
        null=True,
    )
    sn_no_amended = models.CharField(
        verbose_name='№ СЗ с изменениями',
        max_length=255,
        blank=True,
        null=True,
    )
# * Служебная записка
    sn_plan_days = models.SmallIntegerField(
        verbose_name='Комплектовочные План Дней',
        blank=True,
        null=True,
    )
    sn_plan_work_days = models.SmallIntegerField(
        verbose_name='Комплектовочные План Рабочих Дней',
        blank=True,
        null=True,
    )
    sn_plan_date = models.DateField(
        verbose_name='Комплектовочные План Дата',
        blank=True,
        null=True,
    )

# * Комплектовочные
    pickup_plan_days = models.SmallIntegerField(
        verbose_name='Комплектовочные План Дней',
        blank=True,
        null=True,
    )
    pickup_plan_work_days = models.SmallIntegerField(
        verbose_name='Комплектовочные План Рабочих Дней',
        blank=True,
        null=True,
    )
    pickup_plan_date = models.DateField(
        verbose_name='Комплектовочные План Дата',
        blank=True,
        null=True,
    )

# * Отгрузочные
    shipping_plan_days = models.SmallIntegerField(
        verbose_name='Отгрузочные План Дней',
        blank=True,
        null=True,
    )
    shipping_plan_work_days = models.SmallIntegerField(
        verbose_name='Отгрузочные План Рабочих Дней',
        blank=True,
        null=True,
    )
    shipping_plan_date = models.DateField(
        verbose_name='Отгрузочные План Дата',
        blank=True,
        null=True,
    )

# * Конструкторская документация
    design_plan_days = models.SmallIntegerField(
        verbose_name='Конструкторская документация План Дней',
        blank=True,
        null=True,
    )
    design_plan_work_days = models.SmallIntegerField(
        verbose_name='Конструкторская документация План Рабочих Дней',
        blank=True,
        null=True,
    )
    design_plan_date = models.DateField(
        verbose_name='Конструкторская документация План Дата',
        blank=True,
        null=True,
    )

# * Материалы
    material_plan_days = models.PositiveSmallIntegerField(
        verbose_name='Материалы План Дней',
        blank=True,
        null=True,
    )
    material_plan_work_days = models.PositiveSmallIntegerField(
        verbose_name='Материалы План Рабочих Дней',
        blank=True,
        null=True,
    )
    material_plan_date = models.DateField(
        verbose_name='Материалы План Дата',
        blank=True,
        null=True,
    )
# * Готовый заказ
    ready_status = models.BooleanField(
        verbose_name='Готов',
        blank=True,
        null=True,
        default=False,
    )
    produced = models.BooleanField(
        verbose_name='Производится',
        blank=True,
        null=True,
        default=True,
    )
    ready_date = models.DateField(
        verbose_name='Дата окончания',
        blank=True,
        null=True,
    )
    failure_1= models.CharField(
        verbose_name='Отсутствие тех документации',
        max_length=255,
        blank=True,
        null=True,
    )
    failure_2= models.CharField(
        verbose_name='Дефицит материалов',
        max_length=255,
        blank=True,
        null=True,
    )
    failure_3= models.CharField(
        verbose_name='Дефицит мощностей',
        max_length=255,
        blank=True,
        null=True,
    )
    failure_4= models.CharField(
        verbose_name='Нет технологической возможности (аутсорс)',
        max_length=255,
        blank=True,
        null=True,
    )

# * Мета
    class Meta:
        """Meta definition for OnItm."""

        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        """Unicode representation of Order."""
        return ("%s - %s") % (self.order_no, self.product_name)