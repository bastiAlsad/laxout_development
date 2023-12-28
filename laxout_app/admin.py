from django.contrib import admin
from .models import LaxoutUser, Laxout_Exercise, Coupon, IndexesLaxoutUser, IndexesPhysios



admin.site.register(LaxoutUser)
admin.site.register(Coupon)
admin.site.register(Laxout_Exercise)
admin.site.register(IndexesLaxoutUser)
admin.site.register(IndexesPhysios)


