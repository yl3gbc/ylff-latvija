from functools import wraps

from auth.utils import get_current_user


def admin_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        user, error_response, status_code = get_current_user()

        if error_response:
            return error_response, status_code

        if not user.is_admin:
            return {
                "error": "Admin access required",
            }, 403

        return route_function(user, *args, **kwargs)

    return wrapper
