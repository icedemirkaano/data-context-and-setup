from pathlib import Path
import pandas as pd


class Olist:
    """
    The Olist class provides methods to interact with Olist's e-commerce data.

    Methods:
        get_data():
            Loads and returns a dictionary where keys are dataset names (e.g., 'sellers', 'orders')
            and values are pandas DataFrames loaded from corresponding CSV files.

        ping():
            Prints "pong" to confirm the method is callable.
    """
    def get_data(self):
        """
        This function returns a Python dict.
        """
        csv_path = Path("~/.workintech/olist/data/csv").expanduser()
        file_paths = list(csv_path.glob("*.csv"))
        key_names = [file_path.name.replace(".csv", "").replace("olist_", "").replace("_dataset", "") for file_path in file_paths]
        data = {}
        for (key, path) in zip(key_names, file_paths):             # hangi iki liste?
            data[key] = pd.read_csv(path)
        return data

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
