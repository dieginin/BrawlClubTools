from datetime import date

import pyrebase
import pyrebase.pyrebase as pb

from config import DB_CONFIG
from models import Member


class Database:
    __db = pyrebase.initialize_app(DB_CONFIG).database()

    @property
    def __members(self) -> pb.Database:
        return self.__db.child("members")

    @property
    def __former_members(self) -> pb.Database:
        return self.__db.child("former_members")

    def get_members(self) -> list[Member]:
        return sorted(
            [Member.from_dict(m.val()) for m in self.__members.get()],
            key=lambda m: m.trophies,
            reverse=True,
        )

    def save_member(self, member: Member) -> None:
        tag = member.tag.strip("#")
        existing_member_dict = self.__members.child(tag).get().val()

        if existing_member_dict:
            existing_member = Member.from_dict(existing_member_dict)

            updated_member_dict = {
                "tag": member.tag,
                "name": member.name,
                "real_name": (
                    member.real_name if member.real_name else existing_member.real_name
                ),
                "trophies": member.trophies,
                "strikes": member.strikes,
                "birthday": (
                    member.birthday.isoformat()
                    if member.birthday
                    else (
                        existing_member.birthday.isoformat()
                        if existing_member.birthday
                        else None
                    )
                ),
                "phone_number": (
                    member.phone_number
                    if member.phone_number
                    else existing_member.phone_number
                ),
                "club": member.club.to_dict(),
            }

            self.__members.child(tag).update(updated_member_dict)
        else:
            self.__members.child(tag).set(member.to_dict())

    def remove_member(self, member: Member) -> None:
        tag = member.tag.strip("#")
        self.__members.child(tag).remove()

    def add_former_member(self, member: Member) -> None:
        tag = member.tag.strip("#")
        member_dict = member.to_dict()
        member_dict["departure_date"] = date.today().isoformat()
        member_dict["notes"] = None
        self.__former_members.child(tag).set(member_dict)
