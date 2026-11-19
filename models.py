from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    team: Mapped[str] = mapped_column(index=True)
    role: Mapped[str]