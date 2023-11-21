import pytest
from httpx import AsyncClient
import urllib.parse

query_1 = "date=30.08.2035&mail=test1@gmail.com"
result_1 = {'Name of the valid form 1': 'form_name_3'}
query_2 = "mail=test1@gmail.com"
result_2 = {'mail': 'email'}
query_3 = "name_1=test1&phone=+7 999 999 88 99"
result_3 = {'Name of the valid form 1': 'form_name_4'}
query_4 = "phone=phone=+7 999 999 88&date=30.08.2035&mail=test@gmail.com"
result_4 = {'Name of the valid form 1': 'form_name_3'}
query_5 = "name_1=text&phone=+7 999 999 88 77&date=30.08.2035&mail=test@gmail.com"
result_5 = {
    'Name of the valid form 1': 'form_name_1',
    'Name of the valid form 2': 'form_name_2',
    'Name of the valid form 3': 'form_name_3',
    'Name of the valid form 4': 'form_name_4'
}


class TestForm:
    ROOT_URL = '/'

    @pytest.mark.parametrize("query, status_code, result",
                             [(query_1, 200, result_1),
                              (query_2, 200, result_2),
                              (query_3, 200, result_3),
                              (query_4, 200, result_4),
                              (query_5, 200, result_5)
                              ])
    async def test_get_valid_form(self, ac: AsyncClient, query, status_code, result):
        query_decoded = urllib.parse.quote(query)
        response = await ac.post(f"{self.ROOT_URL}get_form?q={query_decoded}")
        assert response.status_code == status_code
        assert response.json() == result
