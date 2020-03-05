from django.db import models

class BaseWorkplan(models.Model):
    """
    Модель дат из производственного плана
    """
    in_id = models.IntegerField(
        verbose_name='in_id',
    )
    start_date = models.DateField(
        verbose_name='Начало работ',
    )
    end_date = models.DateField(
        verbose_name='Конец работ',
    )
    letter = models.CharField(
        verbose_name='Буква',
        max_length=2,
    )
    shop = models.CharField(
        verbose_name='Буква цеха',
        max_length=2,
    )

# * Мета
    class Meta:
        """Meta definition for BaseWorkplan."""

        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        """Unicode representation of BaseWorkplan."""
        return ("%s - %s %s") % (self.in_id, self.letter, self.shop)