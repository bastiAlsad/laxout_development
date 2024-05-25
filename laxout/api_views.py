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
from datetime import date, datetime, timedelta
import math
from uuid import uuid4
import random


@api_view(["POST"])
def autorise_laxout_user(request):
    user_uid = request.data["user_uid"]
    try:
        user = models.LaxoutUser.objects.get(user_uid=user_uid)
    except models.LaxoutUser.DoesNotExist:
        return Response({"details": "user not found"})

    physio_instance = user.created_by

    if not isinstance(physio_instance, User):
        return Response({"details": "physio not found for the given user"})

    try:
        physio_index_instance = models.IndexesPhysios.objects.get(
            created_by=physio_instance.id,
            for_month=datetime.now().month,
            for_year=datetime.now().year,
        )
        physio_index_instance.logins += 1
        physio_index_instance.save()
    except:
        try:
            models.IndexesPhysios.objects.get(
                created_by=physio_instance.id,
                for_month=datetime.now().month,
                for_year=datetime.now().year,
            )
        except:
            try:
                models.PhysioIndexCreationLog.objects.get(
                    created_by=physio_instance.id,
                    for_month=datetime.now().month,
                    for_year=datetime.now().year,
                )
            except:
                models.PhysioIndexCreationLog.objects.create(
                    created_by=physio_instance.id
                )
                models.IndexesPhysios.objects.create(
                    created_by=physio_instance.id, logins=0
                )

    # physio_index_instance.logins += 1
    # physio_index_instance.save()

    token, created = Token.objects.get_or_create(user=physio_instance)
    return Response({"token": token.key})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_username(request):
    user_id = request.headers.get("user_uid")
    decoded_user_uid = unquote(user_id)
    if user_id is None:
        return Response({"method": "forbidden"})
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
    print("anfrage bekommen")
    user_id = request.headers.get("user_uid")
    if user_id is None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    decoded_user_uid = unquote(user_id)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    if user_instance is None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    exercises = []
    order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
        laxout_user_id=user_instance.id
    )
    sorted_list = sorted(order_objects, key=lambda x: x.order)
    for i in sorted_list:
        exercises.append(models.Laxout_Exercise.objects.get(id=i.laxout_exercise_id))

    exercises_ids = []
    for i in exercises:
        exercises_ids.append(i.id)
    print("IDS THAT GET RETURNED:{}".format(exercises_ids))
    serializer = serializers.LaxoutExerciseSerializer(exercises, many=True)
    # print(serializer.data)
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
            created_by=physio_instance.id,
            for_month=datetime.now().month,
            for_year=datetime.now().year,
        )
        physio_index_instance.tests += 1
        physio_index_instance.save()
    except:
        try:
            models.IndexesPhysios.objects.get(
                created_by=physio_instance.id,
                for_month=datetime.now().month,
                for_year=datetime.now().year,
            )
        except:
            try:
                models.PhysioIndexCreationLog.objects.get(
                    created_by=physio_instance.id,
                    for_month=datetime.now().month,
                    for_year=datetime.now().year,
                )
            except:
                models.PhysioIndexCreationLog.objects.create(
                    created_by=physio_instance.id
                )
                models.IndexesPhysios.objects.create(
                    created_by=physio_instance.id, tests=1
                )

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_pain_level(request):
    print(f"VERARSCT CHAT GPT MICH ?! {datetime.now().isocalendar()[1]}")

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
        models.LaxoutUserPains.objects.create(
            created_by=user_instance.id, zero_two=1, admin_id=physio_instance.id
        )
        print("created 2")
    if painlevel >= 3 and painlevel <= 5:
        models.LaxoutUserPains.objects.create(
            created_by=user_instance.id, theree_five=1, admin_id=physio_instance.id
        )
        print("created 5")
    if painlevel >= 6 and painlevel <= 8:
        models.LaxoutUserPains.objects.create(
            created_by=user_instance.id, six_eight=1, admin_id=physio_instance.id
        )
        print("created 6")
    if painlevel >= 9 and painlevel <= 10:
        models.LaxoutUserPains.objects.create(
            created_by=user_instance.id, nine_ten=1, admin_id=physio_instance.id
        )
        print("created 9")
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

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_unique_customer_uid(requsest):
    customer_uid = str(uuid4())
    while models.SovendusCustomerUid.objects.filter(uid=customer_uid).exists():
        customer_uid = str(uuid4())
    return Response({"customer_uid": customer_uid})


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def buy_sovendus_coupon(request):
    user_uid = unquote(request.headers.get("user_uid"))
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    coupon_id = request.data["coupon_id"]
    coupon_instance = models.Coupon.objects.get(id=coupon_id)
    if coupon_instance == None:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    user_instance = models.LaxoutUser.objects.get(user_uid=user_uid)
    old_coins_amount = user_instance.laxout_credits
    if old_coins_amount >= coupon_instance.coupon_price:
        old_coins_amount -= coupon_instance.coupon_price
        user_instance.laxout_credits = old_coins_amount
        user_instance.save()
        return Response(
             status=status.HTTP_200_OK
        )
    return Response(
        {"details": "not enough coins"}, status=status.HTTP_406_NOT_ACCEPTABLE
    )

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
        if user_instance.instruction_in_int == 0:
            user_instance.instruction_in_int = 1
        user_instance.water_drops_count += math.ceil(
            100 / user_instance.instruction_in_int
        )
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


def weeks_since_first_login(first_login):
    today = datetime.today().date()

    if first_login > today:
        raise ValueError("first_login kann nicht in der Zukunft liegen.")

    # Berechnen Sie die Differenz zwischen heute und first_login
    delta = today - first_login

    # Berechnen Sie die Anzahl der Wochen
    weeks = delta.days // 7

    return weeks


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_progress_week(request):
    user_uid = request.headers.get("user_uid")
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    decoded_user_uid = unquote(user_uid)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    week = weeks_since_first_login(user_instance.creation_date)
    print("WEEK{}".format(week))
    return Response({"week": week})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_individual_indexes(request):
    user_uid = request.headers.get("user_uid")
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    decoded_user_uid = unquote(user_uid)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)

    laxout_user_pains_instances = models.LaxoutUserPains.objects.filter(
        created_by=user_instance.id
    )
    print("sfjhkasjfhasf")
    print(len(laxout_user_pains_instances))
    index_labels = []
    month_year_instances = []
    zero_two_pain = []
    theree_five_pain = []
    six_eight_pain = []
    nine_ten_pain = []

    for she in laxout_user_pains_instances:
        append_she = True
        print(she.for_week)
        print(f"month_year_instances{month_year_instances}")
        for i in month_year_instances:
            if (
                i.for_month == she.for_month
                and i.for_year == she.for_year
                and i.for_week == she.for_week
            ):
                append_she = False

        if append_she:
            index_labels.append(she.for_week)
            month_year_instances.append(she)

    average_pain_list_user = []
  

    for i in month_year_instances:
        current_pains = models.LaxoutUserPains.objects.filter(
            created_by=i.created_by,
            for_month=i.for_month,
            for_year=i.for_year,
            for_week=i.for_week,
        )
        print(f"length current pains: {len(current_pains)}")

        zero_two = 0.0
        theree_five = 0.0
        six_eight = 0.0
        nine_ten = 0.0

        zero_two_count = 0.0
        theree_five_count = 0.0
        six_eight_count = 0.0
        nine_ten_count = 0.0

        for ii in current_pains:
            # print(ii.six_eight)
            # print(ii.zero_two)
            # print(ii.theree_five)
            # print(ii.nine_ten)
            if ii.zero_two != 0:
                zero_two += 1
                zero_two_count += 1
            if ii.theree_five != 0:
                theree_five += 4
                theree_five_count += 1
            if ii.six_eight != 0:
                six_eight += 7
                six_eight_count += 1
            if ii.nine_ten != 0:
                nine_ten += 9.5
                nine_ten_count += 1

        if zero_two_count == 0:
            zero_two_count = 1
        if theree_five_count == 0:
            theree_five_count = 1
        if six_eight_count == 0:
            six_eight_count = 1
        if nine_ten_count == 0:
            nine_ten_count = 1

        
        # zero_two = zero_two / zero_two_count
        # theree_five = theree_five / theree_five_count
        # six_eight = six_eight / six_eight_count
        # nine_ten = nine_ten / nine_ten_count

        

        # if zero_two != 0:
        #     devide += 1
        # if theree_five != 0:
        #     devide += 1
        # if six_eight != 0:
        #     devide += 1
        # if nine_ten != 0:
        #     devide += 1
        average_pain = (zero_two + theree_five + six_eight + nine_ten) / len(current_pains)
        average_pain_list_user.append(average_pain)

        print(six_eight)
        print(zero_two)
        print(theree_five)
        print(nine_ten)
        print(average_pain)

    print(f"average_pain_list{average_pain_list_user}")

    return Response({"user_pains": average_pain_list_user})


# tree logik
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def pour_lax_tree(request):
    decoded_user_uid = unquote(request.headers.get("user_uid"))
    if decoded_user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        tree = models.LaxTree.objects.get(id=user.lax_tree_id)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if user.water_drops_count >= 10:
        user.water_drops_count -= 10
        user.save()
        if tree.condition <= 90:
            tree.condition += 10
            tree.save()
        else:
            tree.condition = 100
            tree.save()
    return Response(status=status.HTTP_200_OK)


# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def buy_water_drops(request):
#     decoded_user_uid = unquote(request.headers.get("user_uid"))
#     if decoded_user_uid == None:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#     try:
#         user = models.LaxoutUser.objects.get(user_uid = decoded_user_uid)
#     except:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#     if user.laxout_credits>= 200:
#         user.laxout_credits -= 200
#         user.water_drops_count += 50
#         user.save()
#     return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_condition(request):
    decoded_user_uid = unquote(request.headers.get("user_uid"))
    if decoded_user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        tree = models.LaxTree.objects.get(id=user.lax_tree_id)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"condition": tree.condition}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_water_drops(request):
    decoded_user_uid = unquote(request.headers.get("user_uid"))
    if decoded_user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)

    return Response({"waterdrops": user.water_drops_count}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_success_controll(request):
    decoded_user_uid = unquote(request.headers.get("user_uid"))
    if decoded_user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    better = request.data["better"]
    if better == True:
        print("better")
        models.SuccessControll.objects.create(created_by=user.id, better=True)
    if better == False:
        print("worse")
        models.SuccessControll.objects.create(created_by=user.id, better=False)
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_success_data(request):
    decoded_user_uid = unquote(request.headers.get("user_uid"))
    if decoded_user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)

    better_success_controll_count = len(
        models.SuccessControll.objects.filter(created_by=user.id, better=True)
    )
    worse_success_controll_count = len(
        models.SuccessControll.objects.filter(created_by=user.id, better=False)
    )
    all = models.SuccessControll.objects.filter(created_by=user.id)
    better_return = 0
    worse_return = 0

    if better_success_controll_count != 0:
        better_return = better_success_controll_count / len(all) * 100

    if worse_success_controll_count != 0:
        worse_return = worse_success_controll_count / len(all) * 100

    print("Better return {}".format(better_return))
    print("Worse return {}".format(worse_return))

    return Response(
        {
            "better": int(better_return),
            "worse": int(worse_return),
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_message_chat(request):
    decoded_user_uid = unquote(request.headers.get("user_uid"))
    if decoded_user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    user.admin_has_seen_chat = False
    user.save()
    message = request.data["message"]
    print("message")
    print(message)
    is_sender = request.data["is_sender"]

    models.ChatDataModel.objects.create(
        message=message,
        is_sender=is_sender,
        created_by=user.id,
        admin_id=user.created_by.id,
    )
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_messages(request):
    decoded_user_uid = unquote(request.headers.get("user_uid"))
    if decoded_user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    user.user_has_seen_chat = True
    user.save()
    messages = models.ChatDataModel.objects.filter(created_by=user.id)
    serializer = serializers.LaxoutChatSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_if_user_has_new_messages(request):
    decoded_user_uid = unquote(request.headers.get("user_uid"))
    if decoded_user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    new_message = user.user_has_seen_chat
    return Response({"new_message": new_message}, status=status.HTTP_200_OK)


def inizialize_exercises_for_app_user(user):
    illness = user.note
    exercise_data = models.AiTrainingData.objects.filter(illness=illness).last()
    print(f"Exercise Data {exercise_data}")
    related_exercises = exercise_data.related_exercises.all()
    current_exercises = []
    for i in related_exercises:
        exercise = models.Laxout_Exercise.objects.create(
            execution=models.Uebungen_Models.objects.get(id=i.exercise_id).execution,
            name=models.Uebungen_Models.objects.get(id=i.exercise_id).name,
            dauer=models.Uebungen_Models.objects.get(id=i.exercise_id).dauer,
            videoPath=models.Uebungen_Models.objects.get(id=i.exercise_id).videoPath,
            looping=models.Uebungen_Models.objects.get(id=i.exercise_id).looping,
            added=False,
            instruction="",
            timer=models.Uebungen_Models.objects.get(id=i.exercise_id).timer,
            required=models.Uebungen_Models.objects.get(id=i.exercise_id).required,
            imagePath=models.Uebungen_Models.objects.get(id=i.exercise_id).imagePath,
            appId=models.Uebungen_Models.objects.get(id=i.exercise_id).id,
            onlineVideoPath=models.Uebungen_Models.objects.get(
                id=i.exercise_id
            ).onlineVideoPath,
        )
        user.exercises.add(exercise)
        current_exercises.append(exercise)
    user.save()
    order = 1
    for i in current_exercises:
        models.Laxout_Exercise_Order_For_User.objects.create(
            laxout_user_id=user.id, laxout_exercise_id=i.id, order=order
        )

        order += 1
    print("User exercises")
    print(user.exercises.all())


@api_view(["POST"])
def create_user_through_app(request):
    tree = models.LaxTree.objects.create()
    user_count = len(models.LaxoutUser.objects.all())
    admin_in_charge = models.User.objects.get(username="Testzugang")  # muss existieren
    new_user_uid = str(uuid4())
    while models.LaxoutUser.objects.filter(user_uid=new_user_uid).exists():
        new_user_uid = str(uuid4())
    user = models.LaxoutUser.objects.create(
        user_uid=new_user_uid,
        laxout_user_name=f"user{user_count}",
        created_by=admin_in_charge,
        lax_tree_id=tree.id,
        instruction="3x wöchentlich",
        note="Kursprogramm 1",
        was_created_through_app=True,
    )
    inizialize_exercises_for_app_user(user=user)
    models.ChatDataModel.objects.create(message = "Willkommen bei der Laxout Chat-Funktion. Sollten Sie Fragen zur App oder zu Übungen haben, können Sie diese hier stellen. Viel Spaß beim benutzen der App!", created_by = user.id, admin_id = admin_in_charge.id, is_sender = False)
    note = "Kursprogramm 1"
    print(f"note{note}")
    token, created = Token.objects.get_or_create(user=admin_in_charge)
    return Response({"token": token.key, "user_uid": new_user_uid})

def generate_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(4)])


#web_view

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_web_code(request):
    decoded_user_uid = unquote(request.headers.get("user_uid"))
    if decoded_user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    user = models.LaxoutUser.objects.get(user_uid= decoded_user_uid)
    web_code = generate_code()
    while models.WebCodes.objects.filter(code = web_code).exists():
        web_code = generate_code()
    print(web_code)
    models.WebCodes.objects.create(created_by = user.id, code = web_code)
    return Response({"web_code":web_code}, status=status.HTTP_200_OK)




@api_view(["POST"])
def log_webuser_in(request):
    code = request.data["web_code"]
    print(code)
    try:
        web_code = models.WebCodes.objects.get(code= code)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    web_code.delete()
    user = models.LaxoutUser.objects.get(id= web_code.created_by)
    return Response({"code":user.user_uid}, status=status.HTTP_200_OK)



@api_view(["POST"])
def get_web_workout(request):
    user_id = request.data["user_uid"]
    if user_id is None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    decoded_user_uid = unquote(user_id)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    if user_instance is None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    exercises = []
    order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
        laxout_user_id=user_instance.id
    )
    sorted_list = sorted(order_objects, key=lambda x: x.order)
    for i in sorted_list:
        exercises.append(models.Laxout_Exercise.objects.get(id=i.laxout_exercise_id))

    exercises_ids = []
    for i in exercises:
        exercises_ids.append(i.id)
    # print("IDS THAT GET RETURNED:{}".format(exercises_ids))
    serializer = serializers.LaxoutExerciseSerializer(exercises, many=True)
    # print(serializer.data)
    return Response(serializer.data)



@api_view(["POST"])
def get_web_intruction(request):
    user_uid = request.data["user_uid"]
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    decoded_user_uid = unquote(user_uid)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    instruction = user_instance.instruction
    print(instruction)
    return Response({"instruction": str(instruction)})

@api_view(["POST"])
def get_progress_week_web(request):
    user_uid = request.data["user_uid"]
    if user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    decoded_user_uid = unquote(user_uid)
    user_instance = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    week = weeks_since_first_login(user_instance.creation_date)
    print("WEEK{}".format(week))
    return Response({"week": week})



@api_view(["POST"])
def post_web_progress_conrtroll(request):
    decoded_user_uid = unquote(request.data["user_uid"])
    if decoded_user_uid == None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user = models.LaxoutUser.objects.get(user_uid=decoded_user_uid)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    better = request.data["better"]
    if better == True:
        print("better")
        models.SuccessControll.objects.create(created_by=user.id, better=True)
    if better == False:
        print("worse")
        models.SuccessControll.objects.create(created_by=user.id, better=False)
    return Response(status=status.HTTP_200_OK)



@api_view(["POST"])
def finish_workout_web(request):
    user_uid = unquote(request.data["user_uid"])
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
        if user_instance.instruction_in_int == 0:
            user_instance.instruction_in_int = 1
        user_instance.water_drops_count += math.ceil(
            100 / user_instance.instruction_in_int
        )
        user_instance.save()
    return Response(status=status.HTTP_201_CREATED)

@api_view(["POST"])
def skip_exercise_web(request):
    user_uid = unquote(request.data["user_uid"])
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
# note a skipped exercise

@api_view(["POST"])
def finish_exercise_web(request):
    user_uid = unquote(request.data["user_uid"])
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
def post_pain_level_web(request):
    user_uid = request.data["user_uid"]
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
        models.LaxoutUserPains.objects.create(
            created_by=user_instance.id, zero_two=1, admin_id=physio_instance.id
        )
        print("created 2")
    if painlevel >= 3 and painlevel <= 5:
        models.LaxoutUserPains.objects.create(
            created_by=user_instance.id, theree_five=1, admin_id=physio_instance.id
        )
        print("created 5")
    if painlevel >= 6 and painlevel <= 8:
        models.LaxoutUserPains.objects.create(
            created_by=user_instance.id, six_eight=1, admin_id=physio_instance.id
        )
        print("created 6")
    if painlevel >= 9 and painlevel <= 10:
        models.LaxoutUserPains.objects.create(
            created_by=user_instance.id, nine_ten=1, admin_id=physio_instance.id
        )
        print("created 9")
    return Response(status=status.HTTP_200_OK)