from django.db import models

class ShipmentDates(models.Model):
    """
    Модель Отгрузочных Спецификаций
    """
    in_id = models.IntegerField(
        verbose_name='ИД',
    )
    order_no = models.CharField(
        verbose_name='№ Заказа',
        max_length=255,
        blank=True,
        null=True,
    )
    shipment_plan_start_date = models.DateField(
        verbose_name='Начало по плану',
        blank=True,
        null=True,
    )
    shipment_plan_end_date = models.DateField(
        verbose_name='Окончание по плану',
        blank=True,
        null=True,
    )
    shipment_fact_end_date = models.DateField(
        verbose_name='Окончание по факту',
        blank=True,
        null=True,
    )
    shipment_need = models.BooleanField(
        verbose_name='Нужен ли документ',
        blank=True,
        null=True,
        default=True,
    )
    shipment_dispatcher = models.CharField(
        verbose_name='Диспетчер',
        max_length=255,
        blank=True,
        null=True,
    )
# * Мета
    class Meta:
        """Meta definition for ShipmentDates."""

        verbose_name = 'Отгрузочную Спецификацию (ОС)'
        verbose_name_plural = 'Отгрузочные Спецификации (ОС), даты'

    def __str__(self):
        """Unicode representation of ShipmentDates."""
        return ("%s") % (self.in_id)

class PickupDates(models.Model):
    """
    Модель Комплектовочных Ведомостей
    """
    in_id = models.IntegerField(
        verbose_name='ИД',
    )
    order_no = models.CharField(
        verbose_name='№ Заказа',
        max_length=255,
        blank=True,
        null=True,
    )
    pickup_plan_start_date = models.DateField(
        verbose_name='Начало по плану',
        blank=True,
        null=True,
    )
    pickup_plan_end_date = models.DateField(
        verbose_name='Окончание по плану',
        blank=True,
        null=True,
    )
    pickup_fact_end_date = models.DateField(
        verbose_name='Окончание по факту',
        blank=True,
        null=True,
    )
    pickup_need = models.BooleanField(
        verbose_name='Нужен ли документ',
        blank=True,
        null=True,
        default=True,
    )
    pickup_dispatcher = models.CharField(
        verbose_name='Диспетчер',
        max_length=255,
        blank=True,
        null=True,
    )
# * Мета
    class Meta:
        """Meta definition for PickupDates."""

        verbose_name = 'Комплектовочную Ведомость (КВ)'
        verbose_name_plural = 'Комплектовочные Ведомости (КВ), даты'

    def __str__(self):
        """Unicode representation of PickupDates."""
        return ("%s") % (self.in_id)

class DesignDates(models.Model):
    """
    Модель Конструкторской Документации
    """
    in_id = models.IntegerField(
        verbose_name='in_id',
    )
    order_no = models.CharField(
        verbose_name='№ Заказа',
        max_length=255,
        blank=True,
        null=True,
    )
    design_plan_start_date = models.DateField(
        verbose_name='Начало по плану',
        blank=True,
        null=True,
    )
    design_plan_end_date = models.DateField(
        verbose_name='Окончание по плану',
        blank=True,
        null=True,
    )
    design_fact_end_date = models.DateField(
        verbose_name='Окончание по факту',
        blank=True,
        null=True,
    )
    design_need = models.BooleanField(
        verbose_name='Нужен ли документ',
        blank=True,
        null=True,
        default=False,
    )
    design_dispatcher = models.CharField(
        verbose_name='Диспетчер',
        max_length=255,
        blank=True,
        null=True,
    )
# * Мета
    class Meta:
        """Meta definition for DesignDates."""

        verbose_name = 'Конструкторскую Документацию (КД)'
        verbose_name_plural = 'Конструкторская документация (КД), даты'

    def __str__(self):
        """Unicode representation of DesignDates."""
        return ("%s") % (self.in_id)

class ServiceNoteDates(models.Model):
    """
    Модель Служебных записок
    """
    in_id = models.IntegerField(
        verbose_name='in_id',
    )
    order_no = models.CharField(
        verbose_name='№ Заказа',
        max_length=255,
        blank=True,
        null=True,
    )
    sn_plan_start_date = models.DateField(
        verbose_name='Начало по плану',
        blank=True,
        null=True,
    )
    sn_plan_end_date = models.DateField(
        verbose_name='Окончание по плану',
        blank=True,
        null=True,
    )
    sn_fact_end_date = models.DateField(
        verbose_name='Окончание по факту',
        blank=True,
        null=True,
    )
    sn_need = models.BooleanField(
        verbose_name='Нужен ли документ',
        blank=True,
        null=True,
        default=True,
    )
    sn_dispatcher = models.CharField(
        verbose_name='Диспетчер',
        max_length=255,
        blank=True,
        null=True,
        default='Коваленко И.С.'
    )
# * Мета
    class Meta:
        """Meta definition for DesignDates."""

        verbose_name = 'Служебную записку (СЗ)'
        verbose_name_plural = 'Служебные записки (СЗ), даты'

    def __str__(self):
        """Unicode representation of DesignDates."""
        return ("%s") % (self.in_id)