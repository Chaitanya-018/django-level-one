from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from review.models import Movie_details
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def basic(request):
    return HttpResponse("Hello World")


def movie_info(request):
    movie=request.GET.get("movie")
    date=request.GET.get("date")
    return JsonResponse({"status":"success","result":{"movie_name":movie,"release_date":date}},status=200)


# @csrf_exempt
# def movies(request):
#     # ------------------ GET (READ) ------------------
#     if request.method == "GET":
#         movies = Movie_details.objects.all()
#         data = []

#         for m in movies:
#             data.append({
#                 "id": m.id,
#                 "movie_name": m.movie_name,
#                 "release_date": m.release_date,
#                 "budget": m.budget,
#                 "rating": m.rating,
#                 "stars": "⭐" * int(m.rating)
#             })

#         return JsonResponse({"movies": data}, status=200)
    
#     # if request.method == "GET":
#     #     result = list(Movie_details.objects.values())
#     #     return JsonResponse({"movies": result}, status=200)
    

#     # ------------------ POST (CREATE) ------------------
#     if request.method == "POST":
#         #data = json.loads(request.body) #whenever we send in json format we use this
#         data = request.POST #when we send data in form format we use this

#         rating_value = int(data.get("rating", 0))
#         stars = "⭐" * rating_value

#         movie = Movie_details.objects.create(
#             movie_name=data.get("movie_name"),
#             release_date=data.get("release_date"),
#             budget=data.get("budget"),
#             rating=rating_value
#         )

#         response_data = {
#             "id": movie.id,
#             "movie_name": movie.movie_name,
#             "release_date": movie.release_date,
#             "budget": movie.budget,
#             "rating": movie.rating,
#             "stars": stars
#         }

#         return JsonResponse(response_data, status=200)
    

#     # ------------------ PUT (UPDATE) ------------------
#     if request.method == "PUT":
#         data = json.loads(request.body)
#         movie_id = data.get("id")

#         try:
#             movie = Movie_details.objects.get(id=movie_id)
#         except Movie_details.DoesNotExist:
#             return JsonResponse({"error": "Movie not found"}, status=404)

#         # Update fields
#         movie.movie_name = data.get("movie_name", movie.movie_name)
#         movie.release_date = data.get("release_date", movie.release_date)
#         movie.budget = data.get("budget", movie.budget)
#         movie.rating = int(data.get("rating", movie.rating))
#         movie.save()

#         return JsonResponse({
#             "message": "Movie updated successfully",
#             "movie": {
#                 "id": movie.id,
#                 "movie_name": movie.movie_name,
#                 "release_date": movie.release_date,
#                 "budget": movie.budget,
#                 "rating": movie.rating,
#                 "stars": "⭐" * int(movie.rating)
#             }
#         }, status=200)


#     # ------------------ DELETE ------------------
#     if request.method == "DELETE":
#         data = json.loads(request.body)
#         movie_id = data.get("id")

#         try:
#             movie = Movie_details.objects.get(id=movie_id)
#         except Movie_details.DoesNotExist:
#             return JsonResponse({"error": "Movie not found"}, status=404)

#         movie.delete()

#         return JsonResponse({"message": "Movie deleted successfully"}, status=200)

#     return JsonResponse({"error": "Invalid method"}, status=400)

@csrf_exempt
def movies(request):

    if request.method == "GET":
        Movie_info = Movie_details.objects.all()
        movie_list = []

        for movie in Movie_info:
            movie_list.append({
                "movie_name": movie.movie_name,
                "release_date": movie.release_date,
                "budget": movie.budget,
                "rating": movie.rating
            })

        return JsonResponse({"status": "success", "data": movie_list}, status=200)


    # if request.method=="GET":
    #     Movie_info=Movie_details.objects.all()
    #     movie_list=[]
    #     rating_filter=request.GET.get("rating")
    #     min_bud_filter=request.GET.get("min_budget")
    #     max_bud_filter=request.GET.get("max_budget")
    #     if rating_filter:
    #         Movie_info=Movie_info.filter(rating__gte=float(rating_filter))
    #     for movie in Movie_info:
    #         if min_bud_filter or max_bud_filter:
    #             budget_str=movie.budget.lower().replace("cr","")
    #             budget_value=float(budget_str)
    #             if min_bud_filter and budget_value<=float(min_bud_filter):
    #                 continue
    #             if max_bud_filter and budget_value>=float(max_bud_filter):
    #                 continue                
    #         movie_list.append({
    #             "movie_name":movie.movie_name,
    #             "release_date":movie.release_date,
    #             "budget":movie.budget,
    #             "rating":movie.rating
    #         })
    #     if len(movie_list)==0:
    #         return JsonResponse({"status":"success","message":"no movies found matching the criteria"},status=200)
    #     return JsonResponse({"status":"success","data":movie_list},status=200)
    
    elif request.method=="PUT":
        data=json.loads(request.body)
        print("PUT data:",data) #check the incoming data
        ref_id=data.get("id")  
        print("Reference ID:",ref_id) #check the id coming from the client
        existing_movie=Movie_details.objects.get(id=ref_id)
        print("Existing Movie:",existing_movie)   # check the existing movie object fetched from db   
        if data.get("movie_name"):
            new_movie_name=data.get("movie_name")
            existing_movie.movie_name=new_movie_name
            existing_movie.save() 
        elif data.get("release_date"):
            new_release_date=data.get("release_date")
            existing_movie.release_date=new_release_date
            existing_movie.save()
        elif data.get("budget"):           
            new_budget=data.get("budget")
            existing_movie.budget=new_budget
            existing_movie.save()
        elif data.get("rating"):
            new_rating=data.get("rating")
            existing_movie.rating=new_rating
            existing_movie.save()
        return JsonResponse({"status":"success","message":"movie record updated successfully","data":data},status=200)           
    
    elif request.method=="DELETE":
        data=request.GET.get("id")
        ref_id=int(data)
        existing_movie=Movie_details.objects.get(id=ref_id)
        existing_movie.delete()
        return JsonResponse({"status":"success","message":"movie record deleted successfully"},status=200)
    
    elif request.method=="POST":
        # data=json.loads(request.body) #whwenver we send data in json format we have to use this
        data=request.POST  # when we send data in form format we have to use this        
        print(data.get("movie_name"),"hello")
        movie=Movie_details.objects.create(movie_name=data.get("movie_name"),release_date=data.get("release_date"),budget=data.get("budget"),rating=data.get("rating"))
        return JsonResponse({"status":"success","message":"movie record inserted successfully","data":data},status=200)
    

    return JsonResponse({"status": "failed", "message": "Invalid method"}, status=400)