from django.db import models


class Feedback(models.Model):
    class Meta:
        ordering = ['-id']

    calendardb = models.ForeignKey('calendar_manager.CalendarDb', null=True, blank=True, on_delete=models.CASCADE, )
    content = models.TextField()
    rating_given = models.PositiveSmallIntegerField(null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rate: {self.rating_given}"
