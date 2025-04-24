from django.db import models

sample_states = (
    ('open', 'Опубликована'),
    ('close', 'Закрыта'),
    ('delete', 'Удалена')
)

class Sample(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.DateTimeField()
    name = models.CharField()
    state = models.CharField(choices=sample_states)
    date_create = models.DateTimeField()
    date_update = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='media/images/', null=True)

roles = (
    ('redactor', 'Редактор'),
)

class User(models.Model):
    id = models.AutoField(primary_key=True) #db.Column(db.Integer, primary_key=True)
    username = models.CharField(unique=True) #db.Column(db.String(128), unique=True, nullable=False)
    password_hash = models.CharField()
    role = models.CharField(choices=roles)
    first_name = models.CharField(null=True)
    second_name = models.CharField(null=True)

class SampleUser(models.Model):
    id = models.AutoField(primary_key=True)
    relation = models.CharField()

    user_id = models.ForeignKey('User', models.DO_NOTHING)
    sample = models.ForeignKey('Sample', models.DO_NOTHING)

