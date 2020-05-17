from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=20)  # 攤販的名稱
    store_name = models.CharField(max_length=10)  # 攤販店家的名稱
    phone_number = models.CharField(max_length=20)  # 攤販的電話號碼
    address = models.CharField(max_length=100)  # 攤販的地址

    # 複寫__str__
    def __str__(self):
        return self.vendor_name


class Food(models.Model):
    food_name = models.CharField(max_length=30)  # 食物名稱
    food_price = models.DecimalField(max_digits=3, decimal_places=0)  # 食物價錢
    food_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE) # 哪個攤販做的

    def __str__(self):
        return self.food_name

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Vendor._meta.fields]
    # list_display管理類別Vendor要顯示哪一些內容，() or []都可，只要將該欲顯示的欄位填入即可
    
    # 千萬不要取list_display以外的名稱，因為這是Django制式寫法，
    # 而且 Django看不懂也不會跟你報錯，這對於未來debug而言是一個很大的坑

class Morethanfifty(admin.SimpleListFilter):

	title = _('price')
	parameter_name = 'compareprice' # url最先要接的參數

	def lookups(self, request, model_admin):
		return (
			('>50',_('>50')), # 前方對應下方'>50'(也就是url的request)，第二個對應到admin顯示的文字
			('<=50',_('<=50')),
		)
    # 定義查詢時的過濾條件
	def queryset(self, request, queryset):
		if self.value() == '>50':
			return queryset.filter(price_name__gt=50)
		if self.value() == '<=50':
			return queryset.filter(price_name__lte=50)

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Food._meta.fields]
    # list_display = ['id', 'food_name']
    list_filter = ('food_price', Morethanfifty)
    fields = ['price_name'] # 顯示欄位
    search_fields = ('food_name', 'food_price') # 搜尋欄位
    # ordering = ('price_name',) # 價格 由小到大 排序
    ordering = ('-food_price',) # 新增 -，資料改為 由大到小 排序
