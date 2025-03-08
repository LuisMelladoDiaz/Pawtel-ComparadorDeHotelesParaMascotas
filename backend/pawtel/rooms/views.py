from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import RoomSerializer
from .services import RoomService


class RoomViewSet(viewsets.ViewSet):

    def list(self, request):  # GET /rooms/
        rooms = RoomService.get_all_rooms()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):  # GET /rooms/{id}/
        room = RoomService.get_room_by_id(pk)
        if room:
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):  # POST /rooms/
        room = RoomService.create_room(request.data)
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):  # PUT /rooms/{id}/
        room = RoomService.get_room_by_id(pk)
        if room:
            updated_room = RoomService.update_room(pk, request.data)
            serializer = RoomSerializer(updated_room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):  # PATCH /rooms/{id}/
        room = RoomService.get_room_by_id(pk)
        if room:
            updated_room = RoomService.partial_update_room(pk, request.data)
            serializer = RoomSerializer(updated_room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):  # DELETE /rooms/{id}/
        room = RoomService.get_room_by_id(pk)
        if room:
            RoomService.destroy_room(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
