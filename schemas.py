from pydantic import BaseModel, ConfigDict


class TeamMemberCreate(BaseModel):
    name: str
    team: str
    role: str


class TeamMemberRead(TeamMemberCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int