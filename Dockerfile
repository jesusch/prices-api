
FROM public.ecr.aws/lambda/python:3.9



COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY alcolina alcolina
COPY .env .env

# You can overwrite command in `serverless.yml` template
CMD ["app.handler"]