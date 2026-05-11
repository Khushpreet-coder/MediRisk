from pydantic import BaseModel


class SummaryResponse(BaseModel):
    summary: str

    class Config:
        from_attributes = True