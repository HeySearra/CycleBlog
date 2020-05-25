from user.models import User


class UserInfoJson:
    def __init__(self, user=User()):
        self.name = user.name
        self.sex = user.gender
        self.birthday = '未知' if user.birthday.year == 1900 else user.birthday
        self.organization = user.organization
        self.job = user.position
        self.introduction = user.intro
    
    def pack(self):
        package = {
            'name': self.name,
            'sex': self.sex,
            'birthday': self.birthday,
            'organization': self.organization,
            'job': self.job,
            'introduction': self.introduction,
        }
        return package
