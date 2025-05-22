from pydantic import BaseModel, Field


class Model(BaseModel):
    model : str
    temperature : float
    top_p : float