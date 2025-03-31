from pawtel.app_admins.models import App_Admin
from pawtel.app_admins.serializers import AdminSerializer
from pawtel.app_users.models import UserRole
from pawtel.app_users.services import AppUserService
from pawtel.permission_services import PermissionService


class AdminService:

    # General processes------------------------------------------------------

    @staticmethod
    def general_create_admin(request):
        app_user = AppUserService.general_create_app_user(request)
        admin_created = AdminService.__create_admin(app_user.id)
        output_serializer_data = AdminService.serialize_output_admin(admin_created)
        return output_serializer_data

    # Authorization----------------------------------------------------------
    def authorize_action_admin(request, action_name, admin_id=None):
        role_user = AppUserService.get_current_role_user(request)
        PermissionService.check_permission_admin_service(role_user, action_name)
        if admin_id:
            target_admin = AdminService.__perform_retrieve_admin(role_user, admin_id)

        return role_user

    def __perform_retrieve_admin(role_user, target_admin_id):
        if role_user.user.role == UserRole.ADMIN:
            return AdminService.retrieve_admin(target_admin_id)

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
            raise ValueError("Admin not found")

    @staticmethod
    def retrieve_current_admin(request):
        app_user = AppUserService.get_current_app_user(request)
        admin = AdminService.retrieve_admin_by_user(app_user.id)
        return admin

    @staticmethod
    def retrieve_admin_by_user(app_user_id):
        try:
            return App_Admin.objects.get(user_id=app_user_id)
        except App_Admin.DoesNotExist:
            raise ValueError("Admin not found")

    # POST--------------------------------------------------------

    @staticmethod
    def __create_admin(app_user_id):
        return App_Admin.objects.create(app_user_id=app_user_id)

    # DELETE--------------------------------------------------------

    def validate_admin_deletion(admin_id):
        delete = False
        admin = AdminService.retrieve_admin(admin_id)
        if admin:
            delete = True
        return delete
