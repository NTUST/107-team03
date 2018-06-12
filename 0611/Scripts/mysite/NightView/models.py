from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Food(models.Model):
	food_name = models.CharField(max_length=20) # 店家名
	area = models.DecimalField(max_digits=1,decimal_places=0) 
	# 區域，EX:0=大安區、1=內湖區、2=信義區、3=板橋區、4=中正區
	# 區域，EX:5=新店區、6=新莊區、7=士林區、8=中山區
	address = models.CharField(max_length=100) #地址
	phone = models.CharField(max_length=15) #店家電話
	content = models.CharField(max_length=500,default="請務必輸入內容。") # 內容
	rating = models.DecimalField(max_digits=3,decimal_places=2) # 評價，數值範圍0~5
	price = models.DecimalField(max_digits=3,decimal_places=0) # 平均消費
	image_url = models.CharField(max_length=100) # 圖片網址，要先自己上傳到imgur
	blog_url = models.CharField(max_length=300) # 部落客的文章
	opening_time = models.CharField(max_length=100) #營業時間 EX: 週一至周六 11:00 - 20:30
	create_time = models.DateTimeField(default=timezone.now) # 新增時間，預設now
	is_vegitarian = models.BooleanField(default=False)

	def __str__(self):
		return self.food_name

class Nightview(models.Model):
	view_name = models.CharField(max_length=10) # 夜景名		
	area = models.DecimalField(max_digits=1,decimal_places=0)
	# 區域，EX:0=大安區、1=內湖區、2=信義區、3=板橋區、4=中正區
	# 區域，EX:5=新店區、6=新莊區、7=士林區、8=中山區
	content = models.CharField(max_length=500,default="請務必輸入內容。") # 內容
	address = models.CharField(max_length=100) # 地址
	rating = models.DecimalField(max_digits=1,decimal_places=0) # 評價，數值範圍0~5
	image_url = models.CharField(max_length=100) # 圖片網址，要先自己上傳到imgur
	blog_url = models.CharField(max_length=300) # 部落客的文章
	is_direct = models.BooleanField(default=True) # 是否直達，預設可直達
	walking_time = models.CharField(max_length=20,blank=True) # 步行時間
	view_type = models.DecimalField(max_digits=1,decimal_places=0) # 景點類型，0代表山區，1代表都市
	create_time = models.DateTimeField(default=timezone.now) # 新增時間，預設now
	average_stop_time = models.DecimalField(max_digits=3,decimal_places=0) #平均停留時間

	def __str__(self):
		return self.view_name

class User(AbstractUser):

    food = models.CharField(max_length=500,blank=True) #儲存店家的ID
    nightview = models.CharField(max_length=500,blank=True) #儲存夜景的ID
    is_next = models.CharField(max_length=500,blank=True) #判斷誰先


