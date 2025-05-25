from pydantic import BaseModel, Field


class Model(BaseModel):
    model : str
    temperature : float
    top_p : float


class PromptSetting(BaseModel):
    model: str
    temperature: float
    top_p : float
    prompt_template : str
    use_context : str