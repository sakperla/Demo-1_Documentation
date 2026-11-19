from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import TeamMember
from schemas import TeamMemberCreate, TeamMemberRead


router = APIRouter(prefix="/team", tags=["team"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=TeamMemberRead, status_code=status.HTTP_201_CREATED)
def create_member(member: TeamMemberCreate, db: DatabaseSession) -> TeamMember:
    """Create a team member, commit it, and reload it from the database.

    Args:
        member: The new member's name, team, and role.
        db: The SQLAlchemy session used to persist and reload the record.

    Returns:
        The refreshed TeamMember instance, including its generated ID.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If adding, committing, or refreshing
            the record fails with a SQLAlchemy error.
    """
    record = TeamMember(name=member.name, team=member.team, role=member.role)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[TeamMemberRead])
def list_members(db: DatabaseSession) -> list[TeamMember]:
    return list(db.scalars(select(TeamMember).order_by(TeamMember.id)))


@router.get(
    "/by-team/{team_name}",
    response_model=list[TeamMemberRead],
    responses={status.HTTP_404_NOT_FOUND: {"description": "No members found for this team"}},
)
def list_members_by_team(team_name: str, db: DatabaseSession) -> list[TeamMember]:
    members = list(
        db.scalars(
            select(TeamMember).where(TeamMember.team == team_name).order_by(TeamMember.id)
        )
    )
    if not members:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No members found for this team"
        )
    return members