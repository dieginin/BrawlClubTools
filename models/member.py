from datetime import date
from typing import Any, Optional

import phonenumbers
from phonenumbers import geocoder

from .club import Club


class Member:
    def __init__(
        self,
        tag: str,
        name: str,
        trophies: int,
        club: Club,
        strikes: int = 0,
        real_name: Optional[str] = None,
        birthday: Optional[date] = None,
        phone_number: Optional[str] = None,
    ) -> None:
        self.tag = tag
        self.real_name = real_name
        self.name = name
        self.trophies = trophies
        self.strikes = strikes
        self.birthday = birthday
        self.country = None
        self.description = None
        self.phone_number = self.__format_number(phone_number)
        self.club = club

    def __save(self) -> None:
        from services import Database

        db = Database()
        db.save_member(self)

    def __format_number(self, phone_number: Optional[str]) -> str | None:
        if not phone_number:
            return None

        parsed_phone = phonenumbers.parse(phone_number)
        self.country = geocoder.country_name_for_number(parsed_phone, "es")
        self.description = geocoder.description_for_number(parsed_phone, "es")

        return phonenumbers.format_number(
            parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

    def set_real_name(self, real_name: str) -> None:
        self.real_name = real_name
        self.__save()

    def set_birthday(self, birthday: date) -> None:
        self.birthday = birthday
        self.__save()

    def set_phone_number(self, phone_number: str) -> None:
        self.phone_number = self.__format_number(phone_number)
        self.__save()

    def add_strike(self) -> None:
        self.strikes += 1
        self.__save()

    def reset_strikes(self) -> None:
        self.strikes = 0
        self.__save()

    def to_dict(self) -> dict[str, Any]:
        return {
            "tag": self.tag,
            "name": self.name,
            "real_name": self.real_name,
            "trophies": self.trophies,
            "strikes": self.strikes,
            "birthday": self.birthday.isoformat() if self.birthday else None,
            "phone_number": self.phone_number,
            "club": self.club.to_dict(),
        }

    @staticmethod
    def from_dict(data) -> "Member":
        birthday_str = data.get("birthday")
        birthday = date.fromisoformat(birthday_str) if birthday_str else None

        member = Member(
            tag=data.get("tag"),
            name=data.get("name"),
            real_name=data.get("real_name"),
            trophies=data.get("trophies"),
            strikes=data.get("strikes", 0),
            birthday=birthday,
            club=Club.from_dict(data.get("club")),
        )
        member.phone_number = member.__format_number(data.get("phone_number"))
        return member

    def __eq__(self, other) -> bool:
        if not isinstance(other, Member):
            return False
        return self.tag == other.tag
