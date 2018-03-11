from django.db import models

# Create your models here.

SCANNED_STATUS = (
    ('I', 'Idle'),
    ('P', 'In Progress'),
    ('S', 'Scanned'),
)

class WikipediaPage(models.Model):
    subject = models.CharField(max_length=255)

    url = models.URLField()

    create_date = models.DateTimeField(auto_now_add=True)

    scanned_status = models.CharField(max_length=20, choices=SCANNED_STATUS, default='I')
    scanned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

class Word(models.Model):
    name = models.CharField(max_length=500)
    occurrence = models.IntegerField(default=0)

    def to_json(self):
        json_obj = {
            'name': self.name,
            'count': self.occurrence
        }

        words = Word.objects.all().order_by('-occurrence')

        total = 0
        for indx in range(0, 10):
            total += words[indx].occurrence
            json_obj['percent'] = "{0:.1f}".format(((self.occurrence / total) * 100) * 3)

        return json_obj