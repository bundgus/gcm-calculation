import pandas as pd
import csv


def df_crossjoin(df1, df2, **kwargs):
    # https://gist.github.com/internaut/5a653317688b14fd0fc67214c1352831
    """
    Make a cross join (cartesian product) between two dataframes by using a constant temporary key.
    Also sets a MultiIndex which is the cartesian product of the indices of the input dataframes.
    See: https://github.com/pydata/pandas/issues/5401
    :param df1 dataframe 1
    :param df2 dataframe 2
    :param kwargs keyword arguments that will be passed to pd.merge()
    :return cross join of df1 and df2
    """
    df1['_tmpkey'] = 1
    df2['_tmpkey'] = 1

    res = pd.merge(df1, df2, on='_tmpkey', **kwargs).drop('_tmpkey', axis=1)
    res.index = pd.MultiIndex.from_product((df1.index, df2.index))

    df1.drop('_tmpkey', axis=1, inplace=True)
    df2.drop('_tmpkey', axis=1, inplace=True)

    return res


df = pd.read_csv('EC Air Service Location.csv', header=0, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
df = df.set_index('Air Service Location Code')

air_service_origin = df.loc[:, ['Latitude Decimal Degree Measurement', 'Longitude Decimal Degree Measurement']]
air_service_destination = air_service_origin.copy()
print(air_service_origin.head())
print(air_service_destination.head())

dfx = df_crossjoin(air_service_origin, air_service_destination, suffixes=('_orig', '_dest'))
dfx.index.names = ['Origin', 'Destination']

dfx.to_csv('EC Air Service Location Pairs.csv')
