from django.contrib import admin
from .models import LaxoutUser, Laxout_Exercise, Coupon, IndexesLaxoutUser, IndexesPhysios, DoneExercises, DoneWorkouts, SkippedExercises, Laxout_Exercise_Order_For_User, LaxoutUserPains ,Uebungen_Models



admin.site.register(LaxoutUser)
admin.site.register(Coupon)
admin.site.register(Laxout_Exercise)
admin.site.register(IndexesLaxoutUser)
admin.site.register(IndexesPhysios)
admin.site.register(DoneExercises)
admin.site.register(DoneWorkouts)
admin.site.register(SkippedExercises)
admin.site.register(Laxout_Exercise_Order_For_User)
admin.site.register(LaxoutUserPains)
admin.site.register(Uebungen_Models)
