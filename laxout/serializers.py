from rest_framework import serializers
from laxout_app import models


class LaxoutUSerSerializer(serializers.ModelSerializer):
        class Meta(object):
             model = models.LaxoutUser
             fields = ['__all__']


class LaxoutExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Laxout_Exercise
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
       class Meta(object):
              model = models.Coupon
              fields = "__all__"


class LaxoutUSerInstructionSerializer(serializers.ModelSerializer):
        class Meta(object):
             model = models.LaxoutUser
             fields = ['instruction']

class LaxoutChatSerializer(serializers.ModelSerializer):
      class Meta(object):
            model=  models.ChatDataModel
            fields = "__all__"