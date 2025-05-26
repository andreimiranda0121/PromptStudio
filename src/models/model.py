from pydantic import BaseModel, Field

class PromptSetting(BaseModel):
    email : str
    input : str
    model: str
    temperature: float
    top_p : float
    prompt_template : str
    use_context : str
    prompt_id : str
    