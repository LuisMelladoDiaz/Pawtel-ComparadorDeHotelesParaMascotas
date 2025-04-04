from pawtel.app_admins.models import App_Admin
from pawtel.app_admins.serializers import AdminSerializer
from pawtel.app_users.services import AppUserService
from pawtel.permission_services import PermissionService
from rest_framework.exceptions import AuthenticationFailed, NotFound


class AdminService:

    # General processes------------------------------------------------------

    # Authorization----------------------------------------------------------
    def authorize_action_admin(request, action_name, admin_id=None):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_admin_service(role_user, action_name)
        if admin_id:
            AdminService.retrieve_admin(admin_id)
        return role_user

    # Serialization------------------------------------------------------

    @staticmethod
    def serialize_output_admin(admin, many=False):
        return AdminSerializer(admin, many=many).data

    @staticmethod
    def list_admins():
        return App_Admin.objects.all()

    # GET--------------------------------------------------------

    @staticmethod
    def retrieve_admin(pk):
        try:
            return App_Admin.objects.get(id=pk)
        except App_Admin.DoesNotExist:
            raise NotFound("Administrador no encontrado")

    @staticmethod
    def retrieve_current_admin(request):
        app_user = AppUserService.get_current_app_user(request)
        admin = AdminService.retrieve_admin_by_user(app_user.id)
        return admin

    @staticmethod
    def is_current_user_admin(request):
        try:
            AppUserService.get_current_role_user(request)
            return True
        except (AuthenticationFailed, NotFound):
            return False

    @staticmethod
    def retrieve_admin_by_user(app_user_id):
        try:
            return App_Admin.objects.get(user_id=app_user_id)
        except App_Admin.DoesNotExist:
            raise NotFound("Administrador no encontrado")
