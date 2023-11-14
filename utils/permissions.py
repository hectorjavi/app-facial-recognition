from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def get_user_permissions(user):
    # user permission
    permission_user = {
        permission.id: permission.codename
        for permission in Permission.objects.filter(user__id=user.id).select_related(
            "content_type"
        )
    }
    # user group permission
    group_permissions = Group.objects.filter(user__id=user.id).prefetch_related(
        "permissions__content_type"
    )
    for group in group_permissions:
        permission_user |= {
            permission.id: permission.codename for permission in group.permissions.all()
        }

    return permission_user


def get_all_permision_model(model):
    permission_models = Permission.objects.filter(content_type=model)
    return {
        model_action.id: model_action.codename for model_action in permission_models
    }


def exist_permission_model(model, user, method):
    if user is None or user.is_anonymous:
        return False
    model = ContentType.objects.get_for_model(model)
    current_user_permissions = get_user_permissions(user)
    methods_models = get_all_permision_model(model)
    model_name = model.model

    action_models = {
        "POST": f"add_{model_name}",
        "GET": f"view_{model_name}",
        "PUT": f"change_{model_name}",
        "PATCH": f"change_{model_name}",
        "DELETE": f"delete_{model_name}",
    }

    action_model = {
        key: val for key, val in methods_models.items() if val == action_models[method]
    }
    if action_model is not None:
        return list(action_model.keys())[0] in current_user_permissions
    else:
        return False
