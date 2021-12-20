from rest_framework import generics,viewsets, mixins
from django.http import HttpResponse
import json
from .models import Neighborhood
from .serializers import NeighborhoodSerializer

class get_available_neighborhoods_view(generics.ListAPIView):
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer

class get_neighborhood_data(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def get_neighborhood_data(self, request):
        neighborhood = request.query_params.get('neighborhood', None)

        if neighborhood:
            neighborhoods_data = [
                {
                    "data": {
                        "moradia": {
                            "imageUrl": "https://image.architonic.com/prj2-3/20116834/rua-141-apartment-in-sao-paulo-architonic-3629-01-arcit18.jpg",
                            "imageAlt": "Rear view of modern home with pool",
                            "tag1": "3 banheiros",
                            "tag2": "3 quartos",
                            "isLowPrice": True,
                            "title": "Modern home in city center in the heart of historic Los Angeles",
                            "formattedPrice": "R$1,900.00",
                            "reviewCount": 34,
                            "rating": 1
                        },
                        "transporte": {
                            "imageUrl": "https://image.architonic.com/prj2-3/20116834/rua-141-apartment-in-sao-paulo-architonic-3629-01-arcit18.jpg",
                            "imageAlt": "Rear view of modern home with pool",
                            "tag1": "3 banheiros",
                            "tag2": "3 quartos",
                            "isLowPrice": True,
                            "title": "Modern home in city center in the heart of historic Los Angeles",
                            "formattedPrice": "R$1,900.00",
                            "reviewCount": 34,
                            "rating": 1
                        }
                    },
                    "totalPrice": "1900.00",
                    "cashbackPercentage": "15",
                    # "cashbackValue": "285.00"
                }
            ]

            for neighborhood_data in neighborhoods_data:
                neighborhood_data["cashbackValue"] = "{:.2f}".format(float(neighborhood_data["totalPrice"]) * (float(neighborhood_data["cashbackPercentage"])/100))

            return HttpResponse(content=json.dumps(neighborhoods_data, ensure_ascii=False).encode('utf8'), status=200)
        else:
            return HttpResponse(content=json.dumps({'error':"Bairro não especificado"}, ensure_ascii=False).encode('utf8'), status=400)
