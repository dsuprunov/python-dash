import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from icecream import ic

import config


def main():
    try:
        df = pd.read_csv(config.DATA_CSV_FILE)
        df.replace('?', np.nan, inplace=True)

        engine = create_engine(
            url=config.SQLALCHEMY_URL,
            echo=config.SQLALCHEMY_ECHO
        )

        df.to_sql(name=config.SQLALCHEMY_TEMP_IMPORT_TABLE_NAME, con=engine, index=False, if_exists='replace')

        # ToDo remove temp table from DB after usage / import
    except Exception as e:
        ic(e)


if __name__ == '__main__':
    main()
