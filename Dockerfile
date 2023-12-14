
FROM python:3.11-slim


COPY . .

RUN pip install -r requirements.txt

EXPOSE 5555

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"] 
## docker run -p 5555:5555 helenaukraintseva/vet_service:0.1

