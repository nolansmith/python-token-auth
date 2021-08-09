from services.ma import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "username", "role", "created_on")
