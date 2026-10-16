import httpx
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Aapka unique ledger API URL
LEDGER_URL = "https://exam.sanand.workers.dev/questionData?email=24f2006714%40ds.study.iitm.ac.in&quizSign=QMg2for%2B8NPP0kKJnC%2F6RrQB6TSpSu135tyOdJfhrVKpw9oTNToHdEjnHB1n9c6Wx4EpKQkfqedhvHiescfA1dTv0jkJmWgs%2BJ5JmNQeUFhp2AP4gyyoB0NrMVyqkN2QNcIb1LRtVBjtCLTKre9OIkUt4tQ0pkAQtsfOmCtIsgpx5d55VRl2vgaIwTmNJUOtS%2B%2Fq%2FXkxxANA8vYVYQiPivYu%2FPVUBAocjp1hs72PQC%2BRTXjIY2f6gUxaKfKAFnR4%2Ff51vNRB9iyecDezXZ7TQ5Z4ryN08Wef1enF5T8YnvAwDNuMNVQnzIfAixEtLV7S4HjI3FMWRZmPHdWQWZXN4w%3D%3D&questionId=q-ledger-agent-server&path=/"

async def fetch_ledger_data():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(LEDGER_URL, timeout=10.0)
            data = response.json()
            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], list):
                        return pd.DataFrame(data[key])
            return pd.DataFrame()
        except Exception:
            return pd.DataFrame()

@app.api_route("/", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/answer", methods=["GET", "POST", "OPTIONS"])
async def ledger_agent(request: Request):
    if request.method == "GET":
        return {"status": "Ledger Agent API is running"}
        
    try:
        body = await request.json()
    except Exception:
        body = {}
        
    question = body.get("question", "").lower()
    df = await fetch_ledger_data()

    if df.empty:
        return {"answer": 0}

    ans = 0
    try:
        if "revenue" in question or "total" in question:
            if "amount" in df.columns:
                ans = float(df["amount"].sum())
            elif "price" in df.columns:
                ans = float(df["price"].sum())
        else:
            ans = len(df)
    except Exception:
        ans = 0

    return {"answer": ans}