import asyncio
import aiohttp

from aiohttp_retry import RetryClient

class MercadoPublicoApiService():

    def __init__(self, ticket):
        self.MERCADO_PUBLICO_API_URL = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
        self.MERCADO_PUBLICO_TICKET = ticket
        self.retry_attempts = 10
        self.retry_for_statuses = {500}

    async def get_active_tenders(self):
        params = {
            "ticket": self.MERCADO_PUBLICO_TICKET,
            "estado": "activas"
        }
        try:
            async with RetryClient() as client:
                async with client.get(url=self.MERCADO_PUBLICO_API_URL, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            raise Exception("Request Error: ", e) from None

    async def get_tenders_by_date(self, date):
        params = {
            "ticket": self.MERCADO_PUBLICO_TICKET,
            "fecha": date
        }
        try:
            async with RetryClient() as client:
                async with client.get(
                        url=self.MERCADO_PUBLICO_API_URL,
                        params=params,
                        retry_attempts=self.retry_attempts,
                        retry_for_statuses=self.retry_for_statuses) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            raise Exception("Request Error: ", e) from None

async def main_async():
    mercado_publico_api_service = MercadoPublicoApiService("B326DD3E-B373-4A17-BEB4-E405107E7A4D")
    result = await mercado_publico_api_service.get_active_tenders()
    print(result)

asyncio.run(main_async())