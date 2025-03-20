from django.test.client import Client
from ..client import RestClient
from ..models import Formula
from ..settings import BACKEND_HOST, BACKEND_PORT
def test_formula():
    formula = Formula(content="a^2 + b^2 = c^2")
    assert formula.content == b"a^2 + b^2 = c^2"

async def test_update_dataset():
    """"""
    async with RestClient(BACKEND_HOST, BACKEND_PORT) as client:
        #rep = await client.patch("/blog/api/datasets/1/", {"metadata": "test"})
        rep = await client.patch(link="http://localhost:8000/blog/api/datasets/1/", data={"metadata": "test"})
    print(rep.content)


