from datetime import date

from tinydb import Query, TinyDB

from models import Member

query = Query()


class Database:
    __db = TinyDB("database.json")
    members_table = __db.table("members")
    former_members_table = __db.table("former_members")

    def get_members(self) -> list[Member]:
        return sorted(
            [Member.from_dict(m) for m in self.members_table.all()],
            key=lambda m: m.trophies,
            reverse=True,
        )

    def save_member(self, member: Member) -> None:
        existing_member_dict = self.members_table.get(query.tag == member.tag)

        if existing_member_dict:
            existing_member = Member.from_dict(existing_member_dict)

            updated_member_dict = {
                "tag": member.tag,
                "name": member.name,
                "real_name": (
                    member.real_name if member.real_name else existing_member.real_name
                ),
                "trophies": member.trophies,
                "strikes": (
                    member.strikes if member.strikes else existing_member.strikes
                ),
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

            self.members_table.update(updated_member_dict, query.tag == member.tag)
        else:
            self.members_table.insert(member.to_dict())

    def remove_member(self, member: Member) -> None:
        self.members_table.remove(query.tag == member.tag)

    def add_former_member(self, member: Member) -> None:
        member_dict = member.to_dict()
        member_dict["departure_date"] = date.today().isoformat()
        member_dict["notes"] = None
        self.former_members_table.insert(member_dict)
