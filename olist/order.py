import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        orders = self.data['orders'].copy()

        if is_delivered:
            orders = orders.query("order_status == 'delivered'").copy()

        orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
        orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
        orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

        orders['wait_time'] = (
            orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']
        ) / np.timedelta64(1, 'D')

        orders['expected_wait_time'] = (
            orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']
        ) / np.timedelta64(1, 'D')

        orders['delay_vs_expected'] = (
            (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date'])
            / np.timedelta64(1, 'D')
        ).apply(lambda x: x if x > 0 else 0)

        return orders[['order_id', 'wait_time', 'expected_wait_time',
                       'delay_vs_expected', 'order_status']]

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score, cost_of_review
        """
        reviews = self.data['order_reviews'].copy()
        reviews['dim_is_five_star'] = reviews['review_score'].map(lambda x: 1 if x == 5 else 0)
        reviews['dim_is_one_star'] = reviews['review_score'].map(lambda x: 1 if x == 1 else 0)
        reviews['cost_of_review'] = reviews['review_score'].map({
            1: 100, 2: 50, 3: 40, 4: 0, 5: 0
        })
        return reviews[['order_id', 'dim_is_five_star', 'dim_is_one_star',
                        'review_score', 'cost_of_review']]

    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        items = self.data['order_items'].copy()
        return items.groupby('order_id', as_index=False).agg(
            number_of_items=('order_item_id', 'count')
        )

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        items = self.data['order_items'].copy()
        return items.groupby('order_id', as_index=False).agg(
            number_of_sellers=('seller_id', 'nunique')
        )

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        items = self.data['order_items'].copy()
        return items.groupby('order_id', as_index=False).agg(
            price=('price', 'sum'),
            freight_value=('freight_value', 'sum')
        )

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        training_set = (
            self.get_wait_time(is_delivered)
            .merge(self.get_review_score(), on='order_id')
            .merge(self.get_number_items(), on='order_id')
            .merge(self.get_number_sellers(), on='order_id')
            .merge(self.get_price_and_freight(), on='order_id')
        )

        return training_set.dropna()
