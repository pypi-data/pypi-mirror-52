"""
Copyright 2018 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import datetime as dt

import pandas as pd
import pytest
from pandas.util.testing import assert_frame_equal

from gs_quant.api.gs.data import GsDataApi
from gs_quant.context_base import ContextMeta
from gs_quant.markets import MarketDataCoordinate
from gs_quant.session import GsSession, Environment

test_coordinates = (
    MarketDataCoordinate('Prime', quotingStyle='price', marketDataAsset='335320934'),
    MarketDataCoordinate('IR', marketDataAsset='USD', pointClass='Swap', marketDataPoint=('2Y',),
                         quotingStyle='ATMRate'),
)


def test_coordinates_data(mocker):
    bond_data = [
        {
            'marketDataType': 'Prime',
            'marketDataAsset': '335320934',
            'quotingStyle': 'price',
            'price': 1.0139,
            'time': pd.to_datetime('2019-01-20T01:03:00Z')
        },
        {
            'marketDataType': 'Prime',
            'marketDataAsset': '335320934',
            'quotingStyle': 'price',
            'price': 1.0141,
            'time': pd.to_datetime('2019-01-20T01:08:00Z')
        }
    ]
    swap_data = [
        {
            'marketDataType': 'IR',
            'marketDataAsset': 'USD',
            'pointClass': 'Swap',
            'marketDataPoint': ('2Y',),
            'quotingStyle': 'ATMRate',
            'ATMRate': 0.02592,
            'time': pd.to_datetime('2019-01-20T01:09:45Z')
        }
    ]

    bond_expected_result = pd.DataFrame(
        data={
            'time': [pd.to_datetime('2019-01-20T01:03:00Z'), pd.to_datetime('2019-01-20T01:08:00Z')],
            'marketDataType': ['Prime', 'Prime'],
            'marketDataAsset': ['335320934', '335320934'],
            'quotingStyle': ['price', 'price'],
            'value': [1.0139, 1.0141]
        },
        index=pd.DatetimeIndex(['2019-01-20T01:03:00', '2019-01-20T01:08:00']),
    )

    swap_expected_result = pd.DataFrame(
        data={
            'time': [pd.to_datetime('2019-01-20T01:09:45Z')],
            'marketDataType': ['IR'],
            'marketDataAsset': ['USD'],
            'pointClass': ['Swap'],
            'marketDataPoint': [('2Y',)],
            'quotingStyle': ['ATMRate'],
            'value': [0.02592]
        },
        index=pd.DatetimeIndex(['2019-01-20T01:09:45']),
    )

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', side_effect=[{'responses': [{'data': bond_data}]},
                                                                 {'responses': [{'data': bond_data},
                                                                                {'data': swap_data}]}
                                                                 ])

    coord_data_result = GsDataApi.coordinates_data(coordinates=test_coordinates[0], start=dt.datetime(2019, 1, 2, 1, 0),
                                                   end=dt.datetime(2019, 1, 2, 1, 10))
    assert_frame_equal(coord_data_result, bond_expected_result)

    coords_data_result = GsDataApi.coordinates_data(coordinates=test_coordinates, start=dt.datetime(2019, 1, 2, 1, 0),
                                                    end=dt.datetime(2019, 1, 2, 1, 10), as_multiple_dataframes=True)
    assert len(coords_data_result) == 2
    assert_frame_equal(coords_data_result[0], bond_expected_result)
    assert_frame_equal(coords_data_result[1], swap_expected_result)


def test_coordinate_last(mocker):
    data = {'responses': [
        {'data': [
            {
                'marketDataType': 'Prime',
                'marketDataAsset': '335320934',
                'quotingStyle': 'price',
                'price': 1.0141,
                'time': '2019-01-20T01:08:00Z'
            }
        ]},
        {'data': [
            {
                'marketDataType': 'IR',
                'marketDataAsset': 'USD',
                'pointClass': 'Swap',
                'marketDataPoint': ('2Y',),
                'quotingStyle': 'ATMRate',
                'ATMRate': 0.02592,
                'time': '2019-01-20T01:09:45Z'
            }
        ]}
    ]}

    expected_result = pd.DataFrame(
        data={
            'marketDataType': ['Prime', 'IR'],
            'marketDataAsset': ['335320934', 'USD'],
            'pointClass': [None, 'Swap'],
            'marketDataPoint': [None, ('2Y',)],
            'quotingStyle': ['price', 'ATMRate'],
            'value': [1.0141, 0.02592]
        }
    )

    # mock GsSession
    mocker.patch.object(GsSession.__class__, 'current',
                        return_value=GsSession.get(Environment.QA, 'client_id', 'secret'))
    mocker.patch.object(GsSession.current, '_post', return_value=data)

    result = GsDataApi.coordinates_last(coordinates=test_coordinates, as_of=dt.datetime(2019, 1, 2, 1, 10),
                                        as_dataframe=True)

    assert result.equals(expected_result)


def test_get_coverage_api(mocker):
    test_coverage_data = {'results': [{'gsid': 'gsid1'}]}

    mocker.patch.object(ContextMeta, 'current', return_value=GsSession(Environment.QA))
    mocker.patch.object(ContextMeta.current, '_get', return_value=test_coverage_data)
    data = GsDataApi.get_coverage('MA_RANK')

    assert [{'gsid': 'gsid1'}] == data


if __name__ == "__main__":
    pytest.main(args=["test_data.py"])
