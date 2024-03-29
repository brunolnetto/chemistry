from timy import timer
import pandas as pd
from pydantic import BaseModel
from typing import List

from algorithms import  get_k_best_arbitrary_neighbors, \
    get_k_best_support_based_neighbors, get_k_best_random_neighbors
from extract_transform import get_sets_count_per_items_dict, \
    get_items_neighbors_count
from utils.dataframe import listify_items, get_descriptions

from constants import N_SUGGESTIONS_DEFAULT, \
    N_BEST_NEIGHBORS_DEFAULT, \
    RECOMMENDATION_ALGO_DEFAULT

# Request model
class BasketRequest(BaseModel):
    basket: List[str]

# Response model
class RecommendationResponse(BaseModel):
    recommendation: str

class SVRecommender(object):

    def __init__(
        self, 
        df_: pd.DataFrame,
        sets_column: str,
        items_column: str,
        description_column: str,
        n_suggestions: int = N_SUGGESTIONS_DEFAULT,
        n_best_neighbors: int = N_BEST_NEIGHBORS_DEFAULT
    ):
        if(n_suggestions <= 0 or n_best_neighbors <= 0):
            error_message = 'Number of provided suggestions or best neighbors must be greater than 0!'
            raise ValueError(error_message)

        self.data_dataframe = df_
        
        self.__sets_column = sets_column
        self.__items_column = items_column
        
        self.descriptions_dict = get_descriptions(df_, items_column, description_column)
        self.order_list = listify_items(df_, sets_column, items_column)
        self.orders_per_product_dict = get_sets_count_per_items_dict(df_, sets_column, items_column)
        self.neighbors_dict = {}
        self.n_suggestions = n_suggestions
        self.n_best_neighbors = n_best_neighbors

    def _update_neighbors(self):
        self.neighbors = get_items_neighbors_count(self.data_dataframe, self.__sets_column, self.__items_column)
 
    @timer()
    def suggest(
        self, 
        order: list, 
        method: str = RECOMMENDATION_ALGO_DEFAULT
    ):
        if(len(self.neighbors_dict) == 0):
            error_message = 'You must run method \'_update_neighbors\' before running \'suggest\''
            raise ValueError(error_message)

        methods = ['k_best_arbitrary', 'k_best_random', 'k_best_support']
        if(method == 'k_best_arbitrary'):
            return get_k_best_arbitrary_neighbors(
                order, 
                self.neighbors_dict, 
                self.n_suggestions, 
                self.n_best_neighbors
            )
        
        elif(method == 'k_best_random'):
            return get_k_best_random_neighbors(
                order, 
                self.neighbors_dict, 
                self.n_suggestions, 
                self.n_best_neighbors
            )
        
        elif(method == 'k_best_support'):
            return get_k_best_support_based_neighbors(
                order, 
                self.neighbors_dict, 
                self.orders_per_product_dict, 
                self.n_suggestions, 
                self.n_best_neighbors
            )

        else:
            raise ValueError(f'Métodos disponíveis são: {methods}')    

    def describe(self, item_ids: list):
        described_items = []
        
        for item_id in item_ids:
            try:                
                described_items.append(self.descriptions_dict[item_id])
            except Exception as e:
                described_items.append('')

        return described_items