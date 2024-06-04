import os
import pandas as pd
import json

from IMDB_Extended import IMDB_Extended


# Joy Albertini

def load_json_from_file(path):
    try:
        with open(path, 'r') as file:
            data = json.load(file)  # Load JSON data into a Python dictionary or list
            return data
    except FileNotFoundError:
        print(f"No file found at {path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file at {path}")
        return None


class Film_collector:
    def __init__(self):
        if not os.path.exists("Data"):
            os.makedirs("Data")

    def get(self, id_imdb, force_update=False):
        def convert_to_df_reviews(reviews):
            reviews_df = pd.DataFrame(reviews)
            reviews_df.drop("reviewer_name", axis=1, inplace=True)
            if not reviews_df['rating'].empty:
                reviews_df['rating'] = reviews_df['rating'].apply(
                    lambda x: int(x.split('/')[0]) if pd.notnull(x) and '/' in x else None)
            return reviews_df

        if id_imdb is None:
            return
        directory = f'Data/{id_imdb}'
        film_path = f'{directory}/{id_imdb}_film.json'
        review_path = f'{directory}/{id_imdb}_review.csv'
        if os.path.exists(directory) and not force_update:
            print("Retrieving film data from database")
            film_data_json = load_json_from_file(film_path)
            film_reviews = pd.read_csv(review_path)
            return film_data_json, film_reviews
        else:
            print("Fetching data from IMDB")
            if not os.path.exists(directory):
                os.makedirs(directory)
            film_reviews = convert_to_df_reviews(IMDB_Extended(show_chrome=False).fetch_reviews(id_imdb))
            film_reviews.to_csv(review_path, index=False)

            film_data_json = IMDB_Extended(show_chrome=False).get_by_id(id_imdb)
            with open(film_path, 'w') as json_file:
                json_file.write(film_data_json)

            return film_data_json, film_reviews


if __name__ == "__main__":
    film_collector = Film_collector()
    film_data = film_collector.get('tt12037194', True)
