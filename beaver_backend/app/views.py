from rest_framework import generics,viewsets, mixins
from django.http import HttpResponse
import json
from .models import Neighborhood
from .serializers import NeighborhoodSerializer
from .webscramping.home import get_home_data, return_page
from .webscramping.transport import get_transport_data

class get_available_neighborhoods_view(generics.ListAPIView):
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer

class get_neighborhood_data(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def get_neighborhood_data(self, request):
        neighborhood = request.query_params.get('neighborhood', None)
        maxPrice = request.query_params.get('maxPrice', None)

        if neighborhood:
            print(neighborhood)
            if not maxPrice:
                maxPrice = "3000"

            homes_data = get_home_data(neighborhood, maxPrice)
            
            neighborhoods_data = []

            for home_data in homes_data["apts"]:
                neighborhoods_data.extend([
                    {
                        "data": {
                            "moradia": home_data,
                            "transporte": {
                                "imageUrl": "https://is3-ssl.mzstatic.com/image/thumb/Purple126/v4/13/34/17/13341754-d7c8-3e96-f93e-13c4adac7424/AppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/1200x600wa.png",
                                "imageAlt": "Uber Logo",
                                "tag1": "",
                                "tag2": "",
                                "isLowPrice": True,
                                "title": "Médio de preço do Uber",
                                "formattedPrice": "R$"+str(get_transport_data(neighborhood)["uber"]),
                                "reviewCount": 34,
                                "rating": 1
                            }
                        },
                        "totalPrice": str(float(home_data["formattedPrice"].split("R$")[1]) + get_transport_data(neighborhood)["uber"]),
                        "cashbackPercentage": "15",
                        "cashbackValue": "{:.2f}".format(float(home_data["formattedPrice"].split("R$")[1]) + get_transport_data(neighborhood)["uber"] * 15/100),
                        "link1": "https://quintoandar.com.br/alugar/imovel/"+f"{neighborhood}-recife-pe-brasil/"+f"de-500-a-{maxPrice}-aluguel",
                        "link2": "https://www.uber.com/br/pt-br/"
                    },
                    {
                        "data": {
                            "moradia": home_data,
                            "transporte": {
                                "imageUrl": "https://static.standard.co.uk/2021/03/19/02/991f56e5213b507dbc4004cafcefa65aY29udGVudHNlYXJjaCwxNjE1OTk5MjY2-2.54755675.jpg?width=968&auto=webp&quality=75&crop=968%3A645%2Csmart",
                                "imageAlt": "People cathing public transportation",
                                "tag1": "",
                                "tag2": "",
                                "isLowPrice": True,
                                "title": "Média de preço do transporte público",
                                "formattedPrice": "R$"+str(get_transport_data(neighborhood)["bus_average"]),
                                "reviewCount": 34,
                                "rating": 1
                            }
                        },
                        "totalPrice": str(float(home_data["formattedPrice"].split("R$")[1]) + get_transport_data(neighborhood)["bus_average"]),
                        "cashbackPercentage": "15",
                        "cashbackValue": "{:.2f}".format(float(home_data["formattedPrice"].split("R$")[1]) + get_transport_data(neighborhood)["bus_average"] * 15/100),
                        "link1": "https://quintoandar.com.br/alugar/imovel/"+f"{neighborhood}-recife-pe-brasil/"+f"de-500-a-{maxPrice}-aluguel",
                        "link2": ""
                    }
                ])
            # neighborhoods_data = [
            #     {
            #         "data": {
            #             "moradia": {
            #                 "imageUrl": "https://image.architonic.com/prj2-3/20116834/rua-141-apartment-in-sao-paulo-architonic-3629-01-arcit18.jpg",
            #                 "imageAlt": "Rear view of modern home with pool",
            #                 "tag1": "3 banheiros",
            #                 "tag2": "3 quartos",
            #                 "isLowPrice": True,
            #                 "title": "Modern home in city center in the heart of historic Los Angeles",
            #                 "formattedPrice": "R$1,900.00",
            #                 "reviewCount": 34,
            #                 "rating": 1
            #             },
            #             "transporte": {
            #                 "imageUrl": "https://image.architonic.com/prj2-3/20116834/rua-141-apartment-in-sao-paulo-architonic-3629-01-arcit18.jpg",
            #                 "imageAlt": "Rear view of modern home with pool",
            #                 "tag1": "3 banheiros",
            #                 "tag2": "3 quartos",
            #                 "isLowPrice": True,
            #                 "title": "Modern home in city center in the heart of historic Los Angeles",
            #                 "formattedPrice": "R$1,900.00",
            #                 "reviewCount": 34,
            #                 "rating": 1
            #             }
            #         },
            #         "totalPrice": "1900.00",
            #         "cashbackPercentage": "15",
            #         # "cashbackValue": "285.00",
            #         "link1": "google.com",
            #         "link2": "google.com"
            #     }
            # ]

            # for neighborhood_data in neighborhoods_data:
            #     neighborhood_data["cashbackValue"] = "{:.2f}".format(float(neighborhood_data["totalPrice"]) * (float(neighborhood_data["cashbackPercentage"])/100))

            return HttpResponse(content=json.dumps(neighborhoods_data, ensure_ascii=False).encode('utf8'), status=200)
        else:
            return HttpResponse(content=json.dumps({'error':"Bairro não especificado"}, ensure_ascii=False).encode('utf8'), status=400)
