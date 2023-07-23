from dataclasses import dataclass


@dataclass
class MeetingRequest:
    date: str
    step_number: str
    meeting_number: str
    meeting_title: str
    first_name: str
    last_name: str
    telegram_login: str
