from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse

import json
import requests

from ..services import db_service
from ..services import retrieval_service
from ..services import preprocessing_service
from ..services import classification_service
from ..services import clustering_service
from ..services import timetagging_service

@api_view(['GET'])
def getData(request):
    print(request)
    entity = request.GET.get('entity', None)
    from_date = request.GET.get('from_date', None)
    to_date = request.GET.get('to_date', None)
    num_articles = request.GET.get('num_articles', None)
    parsed_entity = entity.replace(" ", "_").lower()

    '''
    articles = retrieval_service.fetch_articles(entity, from_date, to_date, num_articles)
    sentences = preprocessing_service.preprocess_news(articles)
    db_service.upload_to_db("backend", parsed_entity + "_sentences", sentences, True)
    classification_service.init_classification(parsed_entity)
    clustering_service.init_clustering(parsed_entity)
    timetagging_service.init_tagging(parsed_entity)
    '''

    sentences = db_service.download_df("frontend", "topics_" + parsed_entity)
    data = preprocessing_service.prepare_data_for_frontend(sentences)
    return JsonResponse(data, safe=False)
