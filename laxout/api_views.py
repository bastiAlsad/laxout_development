from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from urllib.parse import unquote
from laxout_app import models
from . import serializers
from django.utils import timezone
from datetime import date, datetime


@api_view(["POST"])
def autorise_laxout_user(request):
    user_uid = request.data["user_uid"]

    try:
        user = models.LaxoutUser.objects.get(user_uid=user_uid)
    except models.LaxoutUser.DoesNotExist:
        return Response({"details": "user not found"})

    physio_instance = user.created_by
    try:
        physio_index_instance = models.IndexesPhysios.objects.get(
            for_month=datetime.now().month
        )
        physio_index_instance.logins += 1
        physio_index_instance.save()
    except:
        models.IndexesPhysios.objects.create(created_by=physio_instance.id, logins=1)

    if not isinstance(physio_instance, User):
        return Response({"details": "physio not found for the given user"})

    token, created = Token.objects.get_or_create(user=physio_instance)
    return Response({"token": token.key})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_username(request):
    user_id = request.headers.get("user_uid")
    decoded_user_uid = unquote(user_id)
    if user_id is None:
        print("kakakakkakakkaka")
    print(user_id)
    print(decoded_user_uid)
    laxout_user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    if laxout_user_instance is None:
        return Response({"method": "forbidden"})
    return Response("Es war{}".format(laxout_user_instance.laxout_user_name))


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_exercises(request):
    user_id = request.headers.get("user_uid")
    if user_id is None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    decoded_user_uid = unquote(user_id)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    if user_instance is None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    exercises = user_instance.exercises.all()
    serializer = serializers.LaxoutExerciseSerializer(exercises, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_laxcoins_amount(request):
    user_uid = request.headers.get("user_uid")
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    decoded_user_uid = unquote(user_uid)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    laxcoins_amount = user_instance.laxout_credits
    return Response({"laxcoins_amount": str(laxcoins_amount)})


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_leistungs_index(request):
    user_uid = request.headers.get("user_uid")
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user_instance = models.LaxoutUser.objects.get(user_uid=user_uid)
    if user_instance == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    index = request.data["index"]
    if index == None:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    index_instance = models.IndexesLaxoutUser.objects.create(
        index=index, created_by=user_instance.id
    )
    if user_instance.last_login.date() != date.today():
        user_instance.indexes.add(index_instance)
        user_instance_coins = user_instance.laxout_credits
        user_instance_coins += 100
        user_instance.laxout_credits = user_instance_coins
        user_instance.last_login = datetime.now()
        user_instance.save()

    physio_instance = user_instance.created_by

    try:
        physio_index_instance = models.IndexesPhysios.objects.get(
            for_month=datetime.now().month
        )
        physio_index_instance.tests += 1
        physio_index_instance.save()
    except:
        models.IndexesPhysios.objects.create(created_by=physio_instance.id, tests=1)

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_pain_level(request):
    user_uid = request.headers.get("user_uid")
    decoded_user_uid = unquote(user_uid)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    if user_instance == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    physio = user_instance.created_by
    pain_level = request.data["pain_level"]
    if pain_level == None:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    physio_instance = models.UserProfile.objects.get(user=physio)

    painlevel = pain_level

    if painlevel <= 2:
        try:
            physio_index_instance = models.IndexesPhysios.objects.get(
                for_month=datetime.now().month
            )
            physio_index_instance.zero_two += 1
            physio_index_instance.save()
        except:
            try:
                models.IndexesPhysios.objects.get(
                    created_by=physio_instance.id, for_month=datetime.now().month
                )
            except:
                models.IndexesPhysios.objects.create(
                    created_by=physio_instance.id, zero_two=1
                )
    if painlevel >= 3 and painlevel <= 5:
        try:
            physio_index_instance = models.IndexesPhysios.objects.get(
                for_month=datetime.now().month
            )
            physio_index_instance.theree_five += 1
            physio_index_instance.save()
        except:
            try:
                models.IndexesPhysios.objects.get(
                    created_by=physio_instance.id, for_month=datetime.now().month
                )
            except:
                models.IndexesPhysios.objects.create(
                    created_by=physio_instance.id, theree_five=1
                )
    if painlevel >= 6 and painlevel <= 8:
        try:
            physio_index_instance = models.IndexesPhysios.objects.get(
                for_month=datetime.now().month
            )
            physio_index_instance.six_eight += 1
            physio_index_instance.save()
        except:
            try:
                models.IndexesPhysios.objects.get(
                    created_by=physio_instance.id, for_month=datetime.now().month
                )
            except:
                models.IndexesPhysios.objects.create(
                    created_by=physio_instance.id, six_eight=1
                )
    if painlevel >= 9 and painlevel <= 10:
        try:
            physio_index_instance = models.IndexesPhysios.objects.get(
                for_month=datetime.now().month
            )
            physio_index_instance.nine_ten += 1
            physio_index_instance.save()
        except:
            try:
                models.IndexesPhysios.objects.get(
                    created_by=physio_instance.id, for_month=datetime.now().month
                )
            except:
                models.IndexesPhysios.objects.create(
                    created_by=physio_instance.id, nine_ten=1
                )

    if painlevel <= 2:
        try:
            user_instance_pains = models.LaxoutUserPains.objects.get(
                created_by=user_instance.id
            )
            user_instance_pains.zero_two += 1
            user_instance_pains.save()
            print("Saved pain 2")
        except:
            try:
                models.LaxoutUserPains.objects.get(
                    created_by=user_instance.id, for_month=datetime.now().month
                )
            except:
                models.LaxoutUserPains.objects.create(
                    created_by=user_instance.id, zero_two=1
                )

    if painlevel >= 3 and painlevel <= 5:
        try:
            user_instance_pains = models.LaxoutUserPains.objects.get(
                created_by=user_instance.id
            )
            user_instance_pains.theree_five += 1
            user_instance_pains.save()
            print("Saved pain 5")
        except:
            try:
                models.LaxoutUserPains.objects.get(
                    created_by=user_instance.id, for_month=datetime.now().month
                )
            except:
                models.LaxoutUserPains.objects.create(
                    created_by=user_instance.id, theree_five=1
                )

    if painlevel >= 6 and painlevel <= 8:
        try:
            user_instance_pains = models.LaxoutUserPains.objects.get(
                created_by=user_instance.id
            )
            user_instance_pains.six_eight += 1
            user_instance_pains.save()
            print("Saved pain 8")
        except:
            try:
                models.LaxoutUserPains.objects.get(
                    created_by=user_instance.id, for_month=datetime.now().month
                )
            except:
                models.LaxoutUserPains.objects.create(
                    created_by=user_instance.id, six_eight=1
                )
    if painlevel >= 9 and painlevel <= 10:
        try:
            user_instance_pains = models.LaxoutUserPains.objects.get(
                created_by=user_instance.id
            )
            user_instance_pains.nine_ten += 1
            user_instance_pains.save()
            print("Saved pain 10")
        except:
            try:
                models.LaxoutUserPains.objects.get(
                    created_by=user_instance.id, for_month=datetime.now().month
                )
            except:
                models.LaxoutUserPains.objects.create(
                    created_by=user_instance.id, nine_ten=1
                )

    return Response(status=status.HTTP_200_OK)


#################################Coupon Logic######################################


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_coupons(request):
    user_uid = request.headers.get("user_uid")
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    decoded_user_uid = unquote(user_uid)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    if user_instance == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    coupons = models.Coupon.objects.all()
    if coupons == None:
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = serializers.CouponSerializer(coupons, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_coupons_for_user(request):
    user_uid = unquote(request.headers.get("user_uid"))
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user_instance = models.LaxoutUser.objects.get(user_uid=user_uid)
    if user_instance == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    coupons = user_instance.coupons.all()
    print("data sended getcouponuser")
    serializer = serializers.CouponSerializer(coupons, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def buy_coupon(request):
    user_uid = unquote(request.headers.get("user_uid"))
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    coupon_id = request.data["coupon_id"]
    coupon_instance = models.Coupon.objects.get(id=coupon_id)
    if coupon_instance == None:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    user_instance = models.LaxoutUser.objects.get(user_uid=user_uid)
    old_coins_amount = user_instance.laxout_credits
    if old_coins_amount > coupon_instance.coupon_price:
        print("sack")
        print(coupon_instance.coupon_price)
        print("This is the old amount {}".format(user_instance.laxout_credits))
        print("This is the coupon price {}".format(coupon_instance.coupon_price))
        old_coins_amount -= coupon_instance.coupon_price
        print("This is the new amount {}".format(old_coins_amount))
        user_instance.laxout_credits = old_coins_amount
        user_instance.coupons.add(coupon_instance)
        user_instance.save()
        return Response(
            {"rabatCode": coupon_instance.rabbat_code}, status=status.HTTP_200_OK
        )
    return Response(
        {"details": "not enough coins"}, status=status.HTTP_406_NOT_ACCEPTABLE
    )


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_coupon_user(request):
    user_uid = unquote(request.headers.get("user_uid"))
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    coupon_id = request.data["coupon_id"]
    coupon_instance = models.Coupon.objects.get(id=coupon_id)
    if coupon_instance == None:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    user_instance = models.LaxoutUser.objects.get(user_uid=user_uid)
    to_delete = user_instance.coupons.get(id=coupon_id)
    user_instance.coupons.remove(to_delete)
    user_instance.save()
    return Response(status=status.HTTP_200_OK)


#################################Coupon Logic######################################


# complete exercise for user
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def finish_exercise(request):
    user_uid = unquote(request.headers.get("user_uid"))
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user_instance = models.LaxoutUser.objects.get(user_uid=user_uid)
    if user_instance == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    exercise_id = request.data["exercise_id"]
    if exercise_id == None:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    models.DoneExercises.objects.create(
        exercise_id=exercise_id, laxout_user_id=user_instance.id
    )
    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def skip_exercise(request):
    user_uid = unquote(request.headers.get("user_uid"))
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user_instance = models.LaxoutUser.objects.get(user_uid=user_uid)
    if user_instance == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    exercise_id = request.data["exercise_id"]
    if exercise_id == None:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    models.SkippedExercises.objects.create(
        skipped_exercise_id=exercise_id, laxout_user_id=user_instance.id
    )
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def finish_workout(request):
    user_uid = unquote(request.headers.get("user_uid"))
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user_instance = models.LaxoutUser.objects.get(user_uid=user_uid)
    if user_instance == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    workout_id = request.data["workout_id"]
    if workout_id == None:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    models.DoneWorkouts.objects.create(
        workout_id=workout_id, laxout_user_id=user_instance.id
    )
    if user_instance.last_login_2.date() != date.today():
        user_instance_coins = user_instance.laxout_credits
        user_instance_coins += 100
        user_instance.laxout_credits = user_instance_coins
        user_instance.last_login_2 = datetime.now()
        user_instance.save()
    return Response(status=status.HTTP_201_CREATED)


# note a skipped exercise


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_intruction(request):
    user_uid = request.headers.get("user_uid")
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    decoded_user_uid = unquote(user_uid)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    instruction = user_instance.instruction
    print(instruction)
    return Response({"instruction": str(instruction)})
