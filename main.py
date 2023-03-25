from fastapi import FastAPI, HTTPException
from DataSender_test import DataSender
from pydantic import BaseModel
from typing import Union

app = FastAPI()

dataSender = DataSender()
dataSender.start()

@app.get("/") 
def read_root():
    res = {
        "systemData":dataSender.get_current_data(),
        "sending":dataSender.running,
        "interval":dataSender.interval
    }
    return res

class change_interval_model(BaseModel):
    interval: Union[float, None] = None
    #name: str

@app.post("/change_interval")
def change_interval(change_interval_model: change_interval_model):
    if not dataSender.change_interval(change_interval_model.interval):
        raise HTTPException(status_code=404)
    return

@app.get("/start_sending")
def start_sending():
    if not dataSender.start_sending():
        raise HTTPException(status_code=404)
    return

@app.get("/stop_sending")
def stop_sending():
    if not dataSender.stop_sending():
        raise HTTPException(status_code=404)
    return