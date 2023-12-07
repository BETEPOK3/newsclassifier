from concurrent import futures
import logging

from natasha import Doc, Segmenter
from pymorphy2 import MorphAnalyzer
from sklearn.multioutput import MultiOutputClassifier
from gensim.models.word2vec import Word2Vec as Word2VecVectorizationModel
import numpy as np

import pickle

import grpc
from schema123.gen.types_pb2 import CategoryPrediction
from schema123.gen.categories_pb2 import PredictCategoriesRequest, PredictCategoriesResponse
from schema123.gen.categories_pb2_grpc import CategoriesServicer, add_CategoriesServicer_to_server

WORD2VEC_LOGISTIC_REGRESSION_CV = "models/word2vec_logistic_regression_cv.dat"
WORD2VEC_VECTORIZATION_MODEL = "models/word2vec_vector.dat"

CATEGORIES_LIST = [
    "Автомобили",
    "Технологии",
    "Политика",
    "Трейлер",
    "Игры",
    "Экономика",
    "Общество",
    "Аниме",
    "Манга",
    "Интернет",
    "Наука",
    "Происшествия",
    "Спорт",
    "Культура",
    "Прочее",
]


class Categories(CategoriesServicer):
    word2vec_model_main: MultiOutputClassifier
    word2vec_model_vector: Word2VecVectorizationModel
    graph: Segmenter
    morph: MorphAnalyzer

    def __init__(self):
        # Загрузка моделей.
        with open(WORD2VEC_LOGISTIC_REGRESSION_CV, 'rb') as f:
            self.word2vec_model_main = pickle.load(f)
        with open(WORD2VEC_VECTORIZATION_MODEL, 'rb') as f:
            self.word2vec_model_vector = pickle.load(f)

        # Инициализация объектов для анализа текста.
        self.graph = Segmenter()
        self.morph = MorphAnalyzer()

    # Реализация API для определения категорий текста.
    def PredictCategories(self, request: PredictCategoriesRequest, context):
        doc = Doc(request.text)
        doc.segment(self.graph)
        normal_words = list()
        for token in doc.tokens:
            word = self.morph.parse(token.text)[0]
            if str(word.tag) != "PNCT" and str(word.tag) != "LATN" and "PRCL" not in str(
                    word.tag) and "PREP" not in str(
                word.tag) and str(word.tag) != "UNKN" and "CONJ" not in str(word.tag) \
                    and "NUMB" not in str(word.tag) and "NUMR" not in str(word.tag):
                normal = word.normal_form
                normal_words.append(normal)
        predict = self.word2vec_model_main.predict_proba([self.vectorize(normal_words)])

        predict_text = [(CATEGORIES_LIST[i], x[0][1]) for i, x in enumerate(predict)]
        filtered_predict = list(filter(lambda x: (x[1] >= 0.5), predict_text))

        return PredictCategoriesResponse(result=[CategoryPrediction(category=x[0], prediction=x[1]) for x in filtered_predict])

    # Векторизация текста.
    def vectorize(self, text):
        words_vecs = [self.word2vec_model_vector.wv[word] for word in text if word in self.word2vec_model_vector.wv]
        if len(words_vecs) == 0:
            return np.zeros(500)
        words_vecs = np.array(words_vecs)
        return words_vecs.mean(axis=0)


def serve():
    port = "8035"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CategoriesServicer_to_server(Categories(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started.")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
