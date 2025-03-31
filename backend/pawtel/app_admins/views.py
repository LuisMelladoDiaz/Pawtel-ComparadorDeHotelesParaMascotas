import inspect

from pawtel.app_admins.models import App_Admin
from pawtel.app_admins.serializers import AdminSerializer
from pawtel.app_admins.services import AdminService
from pawtel.app_users.services import AppUserService
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response


class AdminViewSet(viewsets.ViewSet):
    queryset = App_Admin.objects.all()
    serializer_class = AdminSerializer

    def list(self, request):
        action_name = inspect.currentframe().f_code.co_name
        AdminService.authorize_action_admin(request, action_name)
        admins = AdminService.list_admins()
        output_serializer_data = AdminService.serialize_output_admin(admins, many=True)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        AdminService.authorize_action_admin(request, action_name, pk)
        admin = AdminService.retrieve_admin(pk)
        output_serializer_data = AdminService.serialize_output_admin(admin)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        raise MethodNotAllowed("This operation is forbidden.")

    def update(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        admin = AdminService.authorize_action_admin(request, action_name, pk)
        AppUserService.general_update_app_user(request, admin.user.id)
        admin_updated = AdminService.retrieve_admin(pk)
        output_serializer_data = AdminService.serialize_output_admin(admin_updated)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        action_name = inspect.currentframe().f_code.co_name
        AdminService.authorize_action_admin(request, action_name, pk)
        admin = AdminService.retrieve_admin(pk)
        delete = AdminService.validate_admin_deletion(pk)
        if delete:
            AppUserService.general_delete_app_user(request, admin.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        url_name="retrieve_current_admin",
    )
    def retrieve_current_admin(self, request):
        admin = AdminService.retrieve_current_admin(request)
        output_serializer_data = AdminService.serialize_output_admin(admin)
        return Response(output_serializer_data, status=status.HTTP_200_OK)
