import json
import torch
import numpy as np
import pandas as pd
from math import ceil
from PIL import Image
from tokenize import Comment
from matplotlib import transforms
import torchvision.models as models
from .models import Product,FeatureVector
import torchvision.transforms as transforms
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required



def home(request):
    create_feature_vectors()
    current_user = request.user
    print(current_user)
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}
    return render(request,'index.html',params)




# @login_required
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(
#         request,
#         "product_detail.html",
#         {"product": product},
#     )


 # Calculate similarity and recommend similar products
def recommend_similar_products(clicked_product_id, top_n=4):
    clicked_product = get_object_or_404(Product, pk=clicked_product_id)
    clicked_product_feature_vector = FeatureVector.objects.get(
        product=clicked_product
    )
    clicked_product_feature_vector_list = json.loads(
        clicked_product_feature_vector.feature_vector
    )
    clicked_product_feature_vector_array = np.array(
        clicked_product_feature_vector_list
    )

   
    all_products = Product.objects.filter(category=clicked_product.category).exclude(id=clicked_product_id)


    
    similarity_scores = []
    for product in all_products:
        product_feature_vector = FeatureVector.objects.get(product=product)
        product_feature_vector_list = json.loads(
            product_feature_vector.feature_vector
        )
        product_feature_vector_array = np.array(product_feature_vector_list)

        similarity = cosine_similarity(
            [clicked_product_feature_vector_array],
            [product_feature_vector_array],
        )[0][0]

        similarity_scores.append((product, similarity))

    
    similarity_scores.sort(key=lambda x: x[1], reverse=True)

    
    top_similar_products = [product for product, _ in similarity_scores[:top_n]]
    
    
    
    return top_similar_products


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    

    similar_products = recommend_similar_products(pk)

    context = {
        "product": product,
        "similar_products": similar_products,
    }

    return render(request, "product_detail.html", context)






def extract_features_from_image(image_path):
    
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose(
        [
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    image = transform(image).unsqueeze(0)

    
    model = torch.hub.load("pytorch/vision", "resnet18", pretrained=True)
    model.eval()


    with torch.no_grad():
        features = model(image).squeeze().numpy().tolist()

    return features


def create_feature_vectors():
    
    products = Product.objects.all()

    for product in products:
        
        if FeatureVector.objects.filter(product=product).exists():
            continue  

   
        feature_vector = extract_features_from_image(product.image.path)

     
        feature_vector_obj, created = FeatureVector.objects.get_or_create(
            product=product, defaults={"feature_vector": json.dumps(feature_vector)}
        )

      
        feature_vector_obj.save()




# Redirect to a success page or perform any other actions

    # def get_clicked_product_details(product_id):
    #     product = get_object_or_404(Product, id=product_id)
    #     return product

    # def extract_features_from_image(image):
    #     preprocess = transforms.Compose(
    #         [
    #             transforms.Resize((224, 224)),
    #             transforms.ToTensor(),
    #             transforms.Normalize(
    #                 mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    #             ),
    #         ]
    #     )
    #     image = preprocess(image)
    #     image = image.unsqueeze(0)
    #     feature_vector = model(image)
    #     feature_vector = feature_vector.detach().numpy()
    #     return feature_vector

    # def recommend_similar_products(clicked_product_id, top_n=4):
    #     clicked_product = get_clicked_product_details(clicked_product_id)
    #     clicked_product_image = Image.open(clicked_product.image.path).convert("RGB")
    #     clicked_product_features = extract_features_from_image(clicked_product_image)

    #     all_products = Product.objects.exclude(id=clicked_product_id)

    #     similarity_scores = []
    #     for product in all_products:
    #         product_image = Image.open(product.image.path).convert("RGB")
    #         product_features = extract_features_from_image(product_image)

    #         clicked_product_features_2d = clicked_product_features.reshape(1, -1)
    #         product_features_2d = product_features.reshape(1, -1)

    #         similarity = cosine_similarity(clicked_product_features_2d, product_features_2d)[0][0]
    #         similarity_scores.append((product, similarity))

    #     similarity_scores.sort(key=lambda x: x[1], reverse=True)
    #     similar_products = [product for product, _ in similarity_scores[:top_n]]

    #     return similar_products

    # model = models.vgg16(pretrained=True)
    # model = model.features
    # model.eval()