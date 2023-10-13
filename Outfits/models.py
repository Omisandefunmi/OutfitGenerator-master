from typing import Any

from django.db import models

from django.contrib.auth.models import User

from django.urls import reverse

from . import generate

from . import storage

from PIL import Image

import os

from django.http import JsonResponse

 

# os.path.relpath("C:\\Users\\uyiosa.igbinedion\\OneDrive - Interswitch Limited\Documents\\OutfitGenerator\\media\\outfitgenerator pics")

 

# Create your models here.

class ClothingItem(models.Model):

    # user =   models.CharField(max_length = 20) #models.ForeignKey(User,on_delete=models.CASCADE)

    category = models.CharField(max_length = 100)

    name = models.CharField(max_length = 50)

    image = models.ImageField(default = 'default.jpg',upload_to='clothes_pics')

    user = 'ali'

 

    def __str__(self):

        return "{}'s {}".format(self.user,self.name)

   

    def get_absolute_url(self):

        return reverse('dashboard',args=[0])

   

    def save(self,*args, **kwargs):

        super().save(*args, **kwargs)

 

        #Create Product

        # project_id = "primeval-creek-394208"
        project_id = "primeval-creek-394208"

        location =  "europe-west1"

        product_id = self.user + "_" + str(self.id) + 'new'

        product_set_id = self.user + "_PS"

        product_display_name = self.name

        product_category = "apparel"

        key = "category"

        value = self.category

        generate.create_product(project_id,location,product_id,product_display_name,product_category)

 

        #Add Product to Product Set

        generate.add_product_to_product_set(project_id,location,product_id,product_set_id)

 

        #Add product labels

        generate.update_product_labels(project_id,location,product_id,key,value)

 

        #Upload image to storage

        path = self.image.path

        bucket = "vortex-new-bucket"

        file_name = self.name.replace(" ","") + str(self.id)

        storage.upload_blob(bucket,path,file_name)

 

        #Create Reference Image

        ref_id = "REFIMAGE-" + str(self.id)

        uri = "gs://vortex-new-bucket/" + file_name

        generate.create_reference_image(project_id,location,product_id,ref_id,uri)

        # img = Image.open(self.image)

 

        # if img.height > 300 or img.width > 300:

        #     output_size = (300,300)

        #     img.thumbnail(output_size)

        #     img.save(self.image)

 

        # if 'work'in event:

        #     StyleOne.objects.create(season ='winter')

        #     p1 = PossibleItem.objects.create(category=self.category,name=self.name,image='clothes_pics/'+ os.path.basename(self.image.path) )

        #     StyleOne.objects.last().items.add(p1)

 

        # elif 'casual' in event:

        #     StyleTwo.objects.create(season ='winter')

        #     p1 = PossibleItem.objects.create(category=self.category,name=self.name,image='clothes_pics/'+ os.path.basename(self.image.path) )

        #     StyleOne.objects.last().items.add(p1)

 

        # elif 'casual' in event:

        #     StyleThree.objects.create(season ='winter')

        #     p1 = PossibleItem.objects.create(category=self.category,name=self.name,image='clothes_pics/'+ os.path.basename(self.image.path) )

        #     StyleOne.objects.last().items.add(p1)

       

       

       

       

   

 

class BadOutfit(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    items = models.ManyToManyField(ClothingItem)

 

    def __str__(self):

        return "Outfit:{}, Disliked by {}".format(self.id,self.user)

 

 

class PossibleItem(models.Model):

    category = models.CharField(max_length = 100,default='upper')

    name = models.CharField(max_length = 100,default='shirt')

    image = models.ImageField(default='default.jpg',upload_to='clothes_pics')

 

    def __str__(self):

        return "{}".format(self.name)

   

    # def save(self):

    #     super().save()

    #     img = Image.open(self.image.path)

       

    #     if img.height > 300 or img.width > 300:

    #         output_size = (300,300)

    #         img.thumbnail(output_size)

    #         img.save(self.image.path)

 

 

class StyleOne(models.Model):

    #Alex Costa Youtube Channel

    season = models.CharField(max_length = 100)

    items = models.ManyToManyField(PossibleItem)

    category = models.CharField(max_length = 100)

    name = models.CharField(max_length = 50)

    image = models.ImageField(default = 'default.jpg',upload_to='clothes_pics')

   

    def __str__(self):

        return "Alex Costa outfit #{}".format(self.id)

 

class StyleTwo(models.Model):

    #AlphaM Youtube Channel

    season = models.CharField(max_length = 100)

    items = models.ManyToManyField(PossibleItem)

    category = models.CharField(max_length = 100)

    name = models.CharField(max_length = 50)

    image = models.ImageField(default = 'default.jpg',upload_to='clothes_pics')

   

    def __str__(self):

        return "AlphaM outfit #{}".format(self.id)

 

class StyleThree(models.Model):

    #TMF Youtube Channel

    season = models.CharField(max_length = 100)

    items = models.ManyToManyField(PossibleItem)

    category = models.CharField(max_length = 100)

    name = models.CharField(max_length = 50)

    image = models.ImageField(default = 'default.jpg',upload_to='clothes_pics')

   

    def __str__(self):

        return "TMF outfit #{}".format(self.id)
