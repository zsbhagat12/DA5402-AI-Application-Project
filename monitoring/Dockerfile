FROM python:3.10-slim
WORKDIR /app
COPY exporter.py .
RUN pip install flask psutil
EXPOSE 18000
CMD ["python", "exporter.py"]
