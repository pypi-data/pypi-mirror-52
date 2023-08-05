import git_profiles.utils.messages as msg
from typing import TypeVar

P = TypeVar('P', bound='Profile')


class Profile:
    def __init__(self, name: str, mail: str, skey: str, profile: str) -> None:
        self.profile_name = profile.replace("profile.", "")
        self.user = name.strip() if name else None
        self.mail = mail.strip() if mail else None
        self.skey = skey.strip() if skey else None

    def __str__(self) -> str:
        output = "\tName: {0}\n".format(self.user)
        output += "\tMail: {0}\n".format(self.mail)
        if self.skey:
            output += "\tSigning key: {0}\n".format(self.skey)

        return output

    @classmethod
    def build_profile(cls, title: str) -> P:
        user = Profile.ask(msg.BUILD_USER_INPUT)
        mail = Profile.ask(msg.BUILD_MAIL_INPUT)
        skey = Profile.ask(msg.BUILD_SKEY_INPUT, False)

        profile = cls(user, mail, skey, title)
        return profile

    def update_profile(self) -> None:
        user = Profile.ask(msg.UPDATE_USER_INPUT.format(self.user))
        mail = Profile.ask(msg.UPDATE_MAIL_INPUT.format(self.mail))
        skey = Profile.ask(msg.UPDATE_SKEY_INPUT.format(self.skey), False)

        self.user = user
        self.mail = mail
        self.skey = skey

    @staticmethod
    def ask(message: str, required: bool = True) -> str:
        param = input(message)
        param = param.strip()

        if not param and required:
            print(msg.BUILD_REQUIRED, "\n")
            return Profile.ask(message, required)
        return param
