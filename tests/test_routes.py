import json

import pytest
from httpx import AsyncClient


class TestForm:
    ROOT_URL = '/'

    @pytest.mark.asyncio
    async def test_users_create(self, ac: AsyncClient):
        response = await ac.get(f"{self.ROOT_URL}/")
        assert response.status_code == 200