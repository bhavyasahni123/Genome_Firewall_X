FROM condaforge/miniforge3:latest

WORKDIR /app

COPY environment.yml .
COPY requirements.txt .

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "genomefirewall", "/bin/bash", "-c"]

RUN amrfinder -u

COPY . .

EXPOSE 10000

CMD ["conda", "run", "--no-capture-output", "-n", "genomefirewall", \
     "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "10000"]