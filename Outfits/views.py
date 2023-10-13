from typing import Any, Dict

from django.shortcuts import render,redirect

from django.views.generic import TemplateView,ListView

from django.views.generic.edit import CreateView

from django.contrib.auth.models import User

from django.forms.models import model_to_dict

from django.core import serializers

from .models import ClothingItem, BadOutfit, StyleOne, StyleTwo, StyleThree, PossibleItem

from django.contrib.auth import authenticate,login

from .forms import SignUpForm, ClothingItemForm

from django.http import HttpResponse, HttpRequest,JsonResponse

import random

from . import generate

from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt

import os

import openai

from PIL import Image

import shutil

 

# from django.http import JsonResponse

 

#************************chatgpt endpoint**********************************************

 

openai.api_key = "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"

 

@csrf_exempt
@api_view(['POST'])

def chat_ai(request):

    # print('request.POST:',request.POST)

    # print('request.body:',request.data)

    # prompt =  request.POST.get('prompt')

    if request.POST:

        prompt =  request.POST.get('prompt')

    else:

        prompt = request.data['prompt']

 

    print(prompt)

    model = "text-davinci-003"

    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=50)

    generated_text = response.choices[0].text

 

    return Response({'prompt':prompt,'response':generated_text})

 

#************************image-generation endpoint******************************************

 

@csrf_exempt
@api_view(['POST'])
def image_ai(request):
    if request.POST:
        prompt =  request.POST.get('prompt')
    else:
        prompt = request.data['prompt']
    response = openai.Image.create(
        prompt=prompt,
        n=2,    
        size="256x256",

    )

    output ={}

    data_urls = response["data"]

    for idx, data in enumerate(data_urls):

       url = data['url']

       output['url'+ str(idx)] = url

 

    return Response(output)

 

 

 

 

 

# Create your views here.

class HomePageView(TemplateView):

    template_name = 'index.html'

    def get(self,request):

        return render(request,'index.html',{

            'hey':2

        })

 

def generate_gcp_outfit(user,style,season):

    print('style: ',style)

    if style == 0:

        return [[]]

    outfits = {}

    objects = []

    if style == 1:

        objects = StyleOne.objects.filter(season__icontains = season) #StyleOne

        print('objects from style1: ',objects)

        print('len object:',len(objects))

    elif style == 2:

        objects = StyleTwo.objects.filter(season__icontains = season)

        print('objects from style2: ',objects)

        print('len object:',len(objects))

    elif style == 3:

        objects = StyleThree.objects.filter(season__icontains = season)

        print('objects from style3: ',objects)

        print('len object:',len(objects))

 

 

 

    for count, outfit in enumerate(objects):

        print('count: ',count,' outfit-object:',outfit)

    #     outfits[count] = []

        # for item in outfit.items.all():

        #     project_id = "primeval-creek-394208"

        #     location = "europe-west1"

        #     product_set_id = user + str("_PS") #user.username

        #     product_category = "apparel"

        #     file_path = item.image.path #item.image.path

        #     #print(product_set_id)

        #     filter = "category=" + str(item.category)

        #     #create clothing item from line below/find clothing item

        #     #print(item)

        #     product_id = generate.get_similar_products_file(project_id,location,product_set_id,product_category,file_path,filter)

        #     for my_item in ClothingItem.objects.filter():

        #         if my_item.user == user:

        #             if my_item.id == int(product_id):

        #                 outfits[count].append(my_item)

    #                     #print(my_item.name,my_item.id,product_id)

    #                 #print(product_id,my_item.id)

    #             #print(product_id,my_item.user,my_item.id)

    #             #outfits[count].append(my_item)

    # #print(outfits[key])

    # try:

        # key = random.choice(list(outfits.keys()))

        # print('key:',key)

        # print('outfits[key]:',outfits[key])

        # return [outfits[key],len(outfits),outfits]

        # print('outfit:',outfit)

 

 

    # def pick_bottom(output,outfit):

    #     for cloth in outfit.values():

    #         if 'shoe' in cloth[0].name.lower():

    #             output.append(cloth)

    #             return output

 

    # def pick_dress(object):

    #     output = []

    #     for cloth in object.iterator():

    #         if 'dress' in cloth.name:

    #             output.append(cloth)

    #             return output

 

 

    #         elif 'top' in  cloth.name or 'shirt' in cloth.name :

    #             output.append(cloth)

    #             return pick_bottom(output,outfit)

 

    # def pick_footwear(output):

    #     for cloth in outfit.values():

    #         if 'skirt' in cloth[0].name.lower() or 'trouser' in cloth[0].name.lower():

    #             output.append(cloth)

    #             return output

 

 

 

    # output = pick_dress(objects)

    # output = pick_footwear(output)

 

    print('objects-b4-return',objects)

    return objects

   

    # except IndexError:

    #     return []

 

def insufficient_check(user):

    num_items = 0

    for item in ClothingItem.objects.filter():

        if item.user == user:

            num_items += 1

    return num_items < 2

 

#************************outfit-generation endpoint**********************************************

 

 

@csrf_exempt

@api_view(['POST'])

def dashboardView(request):

    # badoutfit = request.POST.get('Dislike')

    # StyleOne = request.POST.get('Alex Costa Outfits')

    # StyleTwo = request.POST.get('Alpha M Outfits')

    # StyleThree = request.POST.get('TMF Outfits')

    # styleChosen = None

 

    if request.POST:

        event = request.POST.get('event')

        season = request.POST.get('season')

   

    else :

        event = request.data['event']

        season = request.data['season']

 

    if event.lower() == 'work':

        style = 1

    elif event.lower() =='social':

        style =2

    elif event.lower() == 'casual':

        style=3

 

 

    #print(StyleTwo)

    user = 'ali' #request.user

    outfit = generate_gcp_outfit(user,style,season)

    print('outfit: ',outfit)

    #generate_gcp_outfit(user)

    #if StyleOne == 'StyleOne':

    #outfit = generate_gcp_outfit(user,0)

    #if StyleOne == "StyleOne":

     #   outfit = generate_gcp_outfit(user,1)

    #if StyleTwo == "StyleTwo":

    #    print('Alpha')

    #    outfit = generate_gcp_outfit(user,2)

    #if StyleThree == "StyleThree":

    #    print('TMF')

    #    outfit = generate_gcp_outfit(user,3)

    # print('style1: ',StyleOne,' style2: ',StyleTwo,' style3:',StyleThree)

    # badoutfitslist = {}

    # is_bad = True

    # insufficient = insufficient_check(user)

 

    #Checks badoutfits

    # for count,outfits in enumerate(BadOutfit.objects.filter()):

    #     #badoutfitslist[count] = []

    #     if outfits.user == user:

    #         badoutfitslist[count] = []

    #         for item in outfits.items.all():

    #             badoutfitslist[count].append(item)

 

    # #Adds to bad outfit model

    # if badoutfit == 'Dislike':

    #     badoutfits = BadOutfit()

    #     for clothing_item in outfit:

    #         badoutfits.user = request.user

    #         badoutfits.save()

    #         badoutfits.items.add(clothing_item)

               

    #print(badoutfitslist)

    # count = len(badoutfitslist.values())

    # for wear in badoutfitslist.values():

    #     if len(set(wear+outfit)) == len(outfit):

            #all items same, outfit is a bad one

            #If length of badoutfits = length of total outfits, then insufficient

            #if len(badoutfitslist) == outfit[1]:

                #insufficient = True

            #else:

            # if StyleOne == "StyleOne":

            #     outfit = generate_gcp_outfit(user,style)

            # if StyleTwo == "StyleTwo":

            #     outfit = generate_gcp_outfit(user,style)

            # if StyleThree == "StyleThree":

            #     outfit = generate_gcp_outfit(user,style)

 

    output = {}

    print('outfit-just-b4-iterator: ',outfit)

    # print('outfit-iterator:',outfit.))

    for idx, cloth in enumerate(outfit.iterator()): #.values()

        print('cloth:-----',cloth)

        print('cloth.image:',cloth.image,' type(cloth.image):',type(cloth.image))

        link = 'media/' + str(cloth.image)

        output['link'+str(idx)] = link

 

    return Response(output)

 

   

    # if not (style == 1 or style == 2 or style == 3):

    #     styleChosen = False

    # else:

    #     styleChosen = True

 

    # if len(outfit) <= 2:

    #     print('length of outfit : ',len(outfit))

    #     return render(request,'dashboard.html',{'myclothes':outfit,'insufficient':insufficient,'styleChosen':styleChosen,'style':style})

   

   

    # #Fix this so bad outfits aren't generated

    # print('length of outfit : ',len(outfit))

    # print('outfit:',outfit)

    # return render(request,'dashboard.html',{'myclothes':outfit,'insufficient':insufficient,'styleChosen':styleChosen,'style':style})

 

 

# class AddClothes(APIView):

 

 

clothes_attribute = {}

 

@csrf_exempt

@api_view(['POST']) # endpoint - newitem

def add_clothes(request):

        # try:

            if request.POST:

                print('request.POST: ',request.POST)

                category = request.POST.get('category').lower() #tops or bottoms or #footwear

                event = request.POST.get('event') # work church dinner e.t.c

                image = request.POST.get('image') # image path

                seasons = request.POST.get('season')

 

                season = ''

                for s in seasons:

                    season += s.lower()

                print(season)

 

                event = ''

                for s in events:

                    event += s.lower()

                print(event)

 

 

                # clothes_attribute[image] = event

 

                # img = Image.open(image)

                # img_name = os.path.basename(image)

 

                # if img.height > 300 or img.width > 300:

                #     output_size = (300,300)

                #     img.thumbnail(output_size)

                #     print('saving image.....')

                #     img.save('/media/clothes_pics/'+img_name)

                #     print('saved image.....')

 

                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(image)))

                destination_folder = os.path.join(BASE_DIR,'clothes_pics')

                destination_path = os.path.join(destination_folder, os.path.basename(image))

                shutil.copy(image, destination_path)

 

                ClothingItem.objects.create( category = category, name = event, image = image)

 

                if 'work' in event:

                    StyleOne.objects.create(season =season,category = category, name = event, image = image)

                    p1 = PossibleItem.objects.create(category=category,name=event,image='clothes_pics/'+ os.path.basename(image) )

                    StyleOne.objects.last().items.add(p1)

 

                if 'social' in event:

                    StyleTwo.objects.create(season =season,category = category, name = event, image = image)

                    p1 = PossibleItem.objects.create(category=category,name=event,image='clothes_pics/'+ os.path.basename(image) )

                    StyleOne.objects.last().items.add(p1)

 

 

                if 'casual' in event:

                    StyleThree.objects.create(season =season,category = category, name = event, image = image)

                    p1 = PossibleItem.objects.create(category=category,name=event,image='clothes_pics/'+ os.path.basename(image) )

                    StyleOne.objects.last().items.add(p1)

 

                return Response({'status':'success'})

           

  #******************************else starts here ********************************************          

            else :      

                print('request.data: ',request.data)        

                category = request.data['category']

                events = request.data['event']  

                image = request.data['image']  

                seasons = request.data['season']

 

                season = ''

                for s in seasons:

                    season += s.lower()

                print('season :',season)

 

                event = ''

                for s in events:

                    event += s.lower()

                print(event)

 

 

                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(image)))

                destination_folder = os.path.join(BASE_DIR,'clothes_pics')

                destination_path = os.path.join(destination_folder, os.path.basename(image))

                shutil.copy(image, destination_path)

 

                # print(f"Image '{image_name}' copied from '{source_folder}' to '{destination_folder}'.")

 

 

                clothes_attribute[image] = event

 

                # img = Image.open(image)

                # img_name = os.path.basename(image)

 

                # if img.height > 300 or img.width > 300:

                #     output_size = (300,300)

                #     img.thumbnail(output_size)

                #     print('saving image.....')

                #     img.save('/media/clothes_pics/'+img_name)

                #     print('saved image.....')

                #     # image = os.path.relpath(image)

 

                ClothingItem.objects.create(category = category, name = event, image = image)

 

                if 'work' in event:

                    StyleOne.objects.create(season =season,category = category, name = event, image = image)

                    p1 = PossibleItem.objects.create(category=category,name=event,image='clothes_pics/'+ os.path.basename(image) )

                    StyleOne.objects.last().items.add(p1)

 

                if 'social' in event:

                    StyleTwo.objects.create(season =season, category = category, name = event, image = image)

                    p1 = PossibleItem.objects.create(category=category,name=event,image='clothes_pics/'+ os.path.basename(image) )

                    StyleOne.objects.last().items.add(p1)

 

 

                if 'casual' in event:

                    StyleThree.objects.create(season =season, category = category, name = event, image = image)

                    p1 = PossibleItem.objects.create(category=category,name=event,image='clothes_pics/'+ os.path.basename(image) )

                    StyleOne.objects.last().items.add(p1)

               

 

                return Response({'status':'success'})

           

        # except Exception as e:

        #     print(e)

        #     return Response({'status':'fail'})

       

 

#********************************************************************************

 

 

class NewItemView(CreateView):

 

    model = ClothingItem

    # template_name = 'newitem.html'

    #fields = ['category','name','image']

    fields = '__all__'

 

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

    #     context =  super().get_context_data(**kwargs)

    #     context['dropdown'] = ['corporate','casual']

    #     return context

 

class MyClothesView(ListView):

    model = ClothingItem

    #print(ClothingItem.objects.filter().first().user)

    template_name = 'myclothes.html'

    context_object_name = 'clothes'

 

 

@csrf_exempt

@api_view(['GET']) # endpoint - myclothes

def view_clothes(request):

    try:

        output = {}

        outer_output = {}

 

        querySet = ClothingItem.objects.all()

        print(querySet)

        if querySet:

            for idx, elem in enumerate(querySet):

                output['link'+str(idx)] = elem.image.path

                # output['event'+str(idx)] = elem.name

                # output['category'+str(idx)] = elem.category

           

            outer_output['data'] = output

 

        else: # print(elem.name)

            outer_output['data']='Nothig to show'

 

 

        return Response(outer_output) #{'status':200}

 

    except Exception as e :

        print(e)

 

        return Response({'status':400})

 

 

 

 

def signup(request):

    if request.user.is_authenticated:

        return redirect('/')

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            form.save()

            username = form.cleaned_data.get('username')

            project_id = "primeval-creek-394208"

            location = "europe-west1"

            product_set_id = username + "_PS"

            product_set_display_name = username + "_OUTFITS"

            generate.create_product_set(project_id,location,product_set_id,product_set_display_name)

            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username = username,password=raw_password)

            login(request,user)

            return redirect('/')

 

    else:

        form = SignUpForm()

 

    return render(request,'registration/signup.html',{'form':form})