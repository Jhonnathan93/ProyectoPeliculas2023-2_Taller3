from django.shortcuts import render
from dotenv import load_dotenv, find_dotenv
import json
import os
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np
from movie.models import Movie


# Create your views here.
def recommendations(request):
    searchTerm = request.GET.get('searchMovie')
    result = []
    if searchTerm:
        # Cargar la clave de la API de OpenAI desde el archivo .env
        env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'openAI.env')
        load_dotenv(env_file_path)
        openai.api_key  = os.environ['openAI_api_key']
        json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'movie_descriptions_embeddings.json')
        with open(json_file_path, 'r') as file:
            file_content = file.read()
            movies = json.loads(file_content)
            #movies = json.load(file)
        emb = get_embedding(searchTerm, engine='text-embedding-ada-002')
        sim = [cosine_similarity(emb, movie['embedding']) for movie in movies]
        sim = np.array(sim)
        ordered_sim = np.argsort(sim)[-3:][::-1]
        for idx in ordered_sim:
            result.append(movies[idx])
            print(f"Recommended Movie: {movies[idx]['title']}")
    return render(request, 'recommendations.html', {'searchTerm': searchTerm, 'result': result, 'movies': Movie.objects.all()})