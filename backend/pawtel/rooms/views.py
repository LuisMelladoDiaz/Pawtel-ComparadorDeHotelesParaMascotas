from pawtel.rooms.models import Room
from pawtel.rooms.serializers import RoomSerializer
from pawtel.rooms.services import RoomService
from rest_framework import status, viewsets
from rest_framework.response import Response


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request):
        rooms = Room.objects.filter(is_archived=False)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        RoomService.authorize_action_room(request, pk)
        room = RoomService.retrieve_room(pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        input_serializer = RoomService.serialize_input_room_create(request)
        RoomService.validate_create_room(input_serializer)
        room_created = RoomService.create_room(input_serializer)
        output_serializer_data = RoomService.serialize_output_room(room_created)
        return Response(output_serializer_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        RoomService.authorize_action_room(request, pk)
        input_serializer = RoomService.serialize_input_room_update(request, pk)
        RoomService.validate_update_room(pk, input_serializer)
        room_updated = RoomService.update_room(pk, input_serializer)
        output_serializer_data = RoomService.serialize_output_room(room_updated)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        RoomService.authorize_action_room(request, pk)
        input_serializer = RoomService.serialize_input_room_partial_update(request, pk)
        RoomService.validate_partial_update_room(pk, input_serializer)
        room_updated = RoomService.partial_update_room(pk, input_serializer)
        output_serializer_data = RoomService.serialize_output_room(room_updated)
        return Response(output_serializer_data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        RoomService.authorize_action_room(request, pk)
        RoomService.delete_room(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
