FROM python:3

WORKDIR /usr/src/scraper_mercado_publico

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "-u", "./main.py" ]