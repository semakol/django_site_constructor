import datetime
import json
from random import sample

from django.conf import settings
from rest_framework import serializers
from .models import Sample, SampleUser, Image
from django.contrib.auth.models import User
from .common import hash_password

CONTENT_SETTINGS = {
  "header": {
    "sample1": {
      "content": {
        "title0": "Надзаголовок",
        "title1": "Заголовок",
        "title2": "Описание",
        "img1": "/content-img-sample1.png"
      }
    },
    "sample2": {
      "content": {
        "title0": "Надзаголовок",
        "title1": "Заголовок",
        "title2": "Описание"
      },
    },
    "sample3": {
      "content": {
        "title1": "Заголовок",
        "title2": "Описание"
      },
    },
    "sample4": {
      "content": {
        "title1": "Заголовок",
        "title2": "Описание",
        "img1": "/sample-icon2.jpg",
        "img2": "/sample-icon1.jpg"
      }
    }
  },
  "text": {
    "sample1": {
      "content": {
        "title0": "Заголовок",
        "text0": "Текст"
      },
    },
    "sample2": {
      "content": {
        "title0": "Заголовок",
        "text0": "Текст"
      },
    },
    "sample3": {
      "content": {
        "title0": "Заголовок",
        "text0": "Текст1",
        "text1": "Текст2"
      },
    },
    "sample4": {
      "content": {
        "title0": "Заголовок",
        "text0": "Всегда, когда провожу секции, смотрю не на конечный результат, а на ход размышлений. Можно выучить все типы задач, прийти, решить все заготовленные интервьюером задачи за 10 минут и молчать, но это не совсем то, что хочется видеть! Живой ум, поток мыслей, желание рассказать и обсудить своё решение — это то, что хочется видеть в первую очередь. Конечно, есть фактор волнения, который заставляет вас быстрее «закончить» всё это. Но и с ним можно бороться — просто решайте больше, не сдавайтесь даже после неудачных попыток, и тогда удача будет на вашей стороне."
      },
    },
    "sample5": {
      "content": {
        "text0": "Всегда, когда провожу секции, смотрю не на конечный результат, а на ход размышлений. Можно выучить все типы задач, прийти, решить все заготовленные интервьюером задачи за 10 минут и молчать, но это не совсем то, что хочется видеть! Живой ум, поток мыслей, желание рассказать и обсудить своё решение — это то, что хочется видеть в первую очередь. Конечно, есть фактор волнения, который заставляет вас быстрее «закончить» всё это. Но и с ним можно бороться — просто решайте больше, не сдавайтесь даже после неудачных попыток, и тогда удача будет на вашей стороне."
      },
    },
    "sample6": {
      "content": {
        "text0": "Всегда, когда провожу секции, смотрю не на конечный результат, а на ход размышлений. Можно выучить все типы задач, прийти, решить все заготовленные интервьюером задачи за 10 минут и молчать, но это не совсем то, что хочется видеть! Живой ум, поток мыслей, желание рассказать и обсудить своё решение — это то, что хочется видеть в первую очередь. Конечно, есть фактор волнения, который заставляет вас быстрее «закончить» всё это. Но и с ним можно бороться — просто решайте больше, не сдавайтесь даже после неудачных попыток, и тогда удача будет на вашей стороне.",
        "text1": "Всегда, когда провожу секции, смотрю не на конечный результат, а на ход размышлений. Можно выучить все типы задач, прийти, решить все заготовленные интервьюером задачи за 10 минут и молчать, но это не совсем то, что хочется видеть! Живой ум, поток мыслей, желание рассказать и обсудить своё решение — это то, что хочется видеть в первую очередь. Конечно, есть фактор волнения, который заставляет вас быстрее «закончить» всё это. Но и с ним можно бороться — просто решайте больше, не сдавайтесь даже после неудачных попыток, и тогда удача будет на вашей стороне.",
        "text2": "Всегда, когда провожу секции, смотрю не на конечный результат, а на ход размышлений. Можно выучить все типы задач, прийти, решить все заготовленные интервьюером задачи за 10 минут и молчать, но это не совсем то, что хочется видеть! Живой ум, поток мыслей, желание рассказать и обсудить своё решение — это то, что хочется видеть в первую очередь. Конечно, есть фактор волнения, который заставляет вас быстрее «закончить» всё это. Но и с ним можно бороться — просто решайте больше, не сдавайтесь даже после неудачных попыток, и тогда удача будет на вашей стороне."
      },
    },
    "sample7": {
      "content": {
        "title0": "Заголовок",
        "text0": "Текст1",
        "text1": "Текст2",
        "text2": "Текст3",
        "text3": "Текст4"
      },
    },
    "sample8": {
      "content": {
        "title0": "Заголовок",
        "text0": "Текст1",
        "text1": "Текст2",
        "text2": "Текст3",
        "text3": "Текст4"
      },
    },
    "sample9": {
      "content": {
        "title0": "Заголовок",
        "text0": "Текст1",
        "text1": "Текст2",
        "text2": "Текст3",
        "text3": "Текст4"
      },
    },
    "sample10": {
      "content": {
        "title0": "Заголовок",
        "text0": "Текст1",
        "text1": "Текст2",
        "text2": "Текст3",
        "text3": "Текст4"
      },
    }
  },
  "gallery": {
    "sample1": {
      "content": {
        "img1": "none",
        "img2": "none",
        "img3": "none"
      },
    },
    "sample2": {
      "content": {
        "img1": "none",
        "img2": "none"
      },
    },
    "sample3": {
      "content": {
        "img1": "none",
        "img2": "none",
        "img3": "none",
        "img4": "none",
        "img5": "none",
        "img6": "none",
        "isGrid": True
      },
    },
    "sample4": {
      "content": {
        "img1": "none",
        "img2": "none",
        "img3": "none",
        "img4": "none",
        "img5": "none",
        "isInfinite": True
      },
    },
    "sample5": {
      "content": {
        "img1": "none"
      },
    }
  },
  "button": {
    "sample1": {
      "content": {
        "text": "Кнопка",
        "link": "#"
      },
    },
    "sample2": {
      "content": {
        "text": "Кнопка",
        "link": "#"
      },
    },
    "sample3": {
      "content": {
        "text": "Кнопка",
        "link": "#"
      },
    },
    "sample4": {
      "content": {
        "text": "Кнопка",
        "link": "#"
      },
    },
    "sample5": {
      "content": {
        "text": "Кнопка",
        "link": "#"
      },
    },
    "sample6": {
      "content": {
        "text": "Кнопка",
        "link": "#"
      },
    },
    "sample7": {
      "content": {
        "text": "Кнопка",
        "link": "#"
      },
    },
    "sample8": {
      "content": {
        "text": "Кнопка",
        "link": "#"
      },
    }
  },
  "contacts": {
    "sample1": {
      "content": {
        "title0": "Контакты",
        "link0": "#",
        "link1": "#",
        "link2": "#"
      },
    },
    "sample2": {
      "content": {
        "title0": "Контакты",
        "title1": "+7 (909) 000 00 00",
        "title2": "IvanovIvan2000@gmail.com",
        "title3": "г. Екатеринбург, ул. Мира, 19"
      },
    },
    "sample3": {
      "content": {
        "link0": "#",
        "link1": "#",
        "link2": "#",
        "isBlack": True
      },
    },
    "sample4": {
      "content": {
        "link0": "#",
        "link1": "#",
        "link2": "#",
        "isBlack": True,
        "withMail": True
      },
    },
    "sample5": {
      "content": {
        "title0": "Контакты",
        "title1": "+7 (909) 000 00 00",
        "title2": "IvanovIvan2000@gmail.com",
        "title3": "г. Екатеринбург, ул. Мира, 19",
        "withMap": True
      },
    }
  },
  "video": {
    "sample1": {
      "content": {
        "video": "none"
      },
    },
    "sample2": {
      "content": {
        "videoLink": "none"
      },
    }
  }
}

class GreetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    second_name = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'second_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        if validated_data.get('second_name'):
            validated_data['last_name'] = validated_data.pop('second_name')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class SampleSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False, default='')
    sample_data = serializers.CharField(required=False)
    user_id = serializers.IntegerField(required=False)
    temp = serializers.BooleanField(required=True)

    class Meta:
        model = Sample
        fields = ['sample_data', 'name', 'state', 'image', 'user_id', 'temp']

    def create(self, validated_data):
        if validated_data['temp']:
            data = json.loads(validated_data['sample_data'])
            for block in data:
                if not block.get('data') and not block['data'].get('content'):
                    continue
                type = block.get('type')
                sample = block.get('sample')
                block['data']['content'] = CONTENT_SETTINGS[type][sample]['content']
            vd_temp = json.dumps(data)
            sample = Sample.objects.create(
                name = validated_data['name'],
                data = vd_temp,
                state = 'temp',
                image = validated_data['image'],
                date_create = datetime.datetime.utcnow(),
                date_update = datetime.datetime.utcnow()
            )
            user = User.objects.get(id=validated_data['user_id'])
            sampleUser = SampleUser.objects.create(
                relation = 'creator',
                user_id = user,
                sample = sample
            )
        sample = Sample.objects.create(
            name=validated_data['name'],
            data=validated_data['sample_data'],
            state=validated_data['state'],
            image=validated_data['image'],
            date_create=datetime.datetime.utcnow(),
            date_update=datetime.datetime.utcnow()
        )
        user = User.objects.get(id=validated_data['user_id'])
        sampleUser = SampleUser.objects.create(
            relation='creator',
            user_id=user,
            sample=sample
        )
        return sample

    def update(self, instance, validated_data):
        if validated_data['temp']:
            data = json.loads(validated_data['sample_data'])
            for block in data:
                if not block.get('data') and not block['data'].get('content'):
                    continue
                type = block.get('type')
                sample = block.get('sample')
                block['data']['content'] = CONTENT_SETTINGS[type][sample]['content']
            vd_temp = json.dumps(data)
            sample = Sample.objects.create(
                name = validated_data['name'],
                data = vd_temp,
                state = 'temp',
                image = validated_data['image'],
                date_create = datetime.datetime.utcnow(),
                date_update = datetime.datetime.utcnow()
            )
            user = User.objects.get(id=validated_data['user_id'])
            sampleUser = SampleUser.objects.create(
                relation = 'creator',
                user_id = user,
                sample = sample
            )
        for key, item in validated_data.items():
            if key == 'sample_data':
                setattr(instance, 'data', item)
            elif key == 'image' and item == '' or key == 'user_id':
                continue
            else:
                setattr(instance, key, item)
        instance.date_update = datetime.datetime.utcnow()
        instance.save()
        return instance

class SampleStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sample
        fields = ['state']

    def update(self, instance, validated_data):
        instance.state = validated_data['state']
        instance.save()
        return instance

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

    def create(self, validated_data):
        image = Image.objects.create(**validated_data)
        return image


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, min_length=6)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'role', 'first_name', 'second_name']
#         extra_kwargs = {
#             'first_name': {'required': False},
#             'second_name': {'required': False}
#         }
#
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             password_hash=hash_password(validated_data['password']),
#             role=validated_data['role'],
#             first_name=validated_data['first_name'],
#             second_name=validated_data['second_name']
#         )
#         return user

