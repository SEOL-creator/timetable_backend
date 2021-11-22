from django.db import models


class Meal(models.Model):
    date = models.DateField()

    class Type(models.IntegerChoices):
        BREAKFAST = 1, "조식"
        LUNCH = 2, "중식"
        DINNER = 3, "석식"

    type = models.IntegerField(
        verbose_name="식사명", choices=Type.choices, default=Type.LUNCH
    )

    number_of_people = models.IntegerField(verbose_name="급식인원수")
    calories = models.IntegerField(verbose_name="칼로리")

    def __str__(self):
        return f"""{self.date} {self.get_type_display()}"""

    class Meta:
        ordering = ["-date", "-type"]


class MealItem(models.Model):
    meal = models.ForeignKey(Meal, related_name="meal_item", on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    allergy_codes = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return f"""{self.meal.date} {self.meal.get_type_display()} {self.name}"""
