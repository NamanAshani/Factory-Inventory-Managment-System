# signal runs after migrations
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# import User and Group models
from django.contrib.auth.models import User, Group


@receiver(post_migrate)
def create_default_users(sender, **kwargs):

    # create roles (groups)
    roles = [
        "Management Director",
        "Management Head",
        "Dispatch Head",
        "Account Head",
        "Marketing Head",
        "Purchase Head",
        "Logistic Head",
    ]

    # create groups safely
    for role in roles:
        Group.objects.get_or_create(name=role)

    users_data = [
        ("director", "director@123", "Management Director"),
        ("managment", "managment@123", "Management Head"),
        ("dispatch", "dispatch@123", "Dispatch Head"),
        ("account", "account@123", "Account Head"),
        ("marketing", "marketing@123", "Marketing Head"),
        ("purchase", "purchase@123", "Purchase Head"),
    ]

    # loop through user list
    for username, password, role in users_data:

        # check if user already exists
        if not User.objects.filter(username=username).exists():

            # create new user
            user = User.objects.create_user(
                username=username,
                password=password
            )

            # add user to group
            group = Group.objects.get(name=role)
            user.groups.add(group)

            # save user
            user.save()
