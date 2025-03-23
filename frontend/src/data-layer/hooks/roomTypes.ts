import { useQuery, useMutation } from '@tanstack/vue-query';
import { ref } from 'vue';
import {
  fetchRoomTypeById,
  fetchAllRoomTypes,
  createRoomType,
  updateRoomType,
  partialUpdateRoomType,
  deleteRoomType,
  checkRoomTypeAvailability,
  fetchHotelOfRoomType,
} from '@/data-layer/api/roomTypes';

export const useGetRoomTypeById = (roomTypeId: number) => {
  return useQuery({
    queryKey: ['room-type', roomTypeId],
    queryFn: () => fetchRoomTypeById(roomTypeId),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useGetAllRoomTypes = () => {
  return useQuery({
    queryKey: ['room-types'],
    queryFn: () => fetchAllRoomTypes(),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useCreateRoomType = () => {
  return useMutation({
    mutationFn: (data: {
      name: string;
      description: string;
      capacity: number;
      num_rooms: number;
      price_per_night: number;
      pet_type: string;
      hotel: number;
    }) => createRoomType(data),
  });
};

export const useUpdateRoomType = () => {
  return useMutation({
    mutationFn: (data: { roomTypeId: number; roomTypeData: { name: string; description: string; capacity: number; num_rooms: number; price_per_night: number } }) =>
      updateRoomType(data.roomTypeId, data.roomTypeData),
  });
};

export const usePartialUpdateRoomType = () => {
  return useMutation({
    mutationFn: (data: { roomTypeId: number; partialData: Partial<RoomType> }) =>
      partialUpdateRoomType(data.roomTypeId, data.partialData),
  });
};

export const useDeleteRoomType = () => {
  return useMutation({
    mutationFn: (roomTypeId: number) => deleteRoomType(roomTypeId),
  });
};

export const useCheckRoomTypeAvailability = () => {
  return useMutation({
    mutationFn: (data: { roomTypeId: number; startDate: string; endDate: string }) =>
      checkRoomTypeAvailability(data.roomTypeId, data.startDate, data.endDate),
  });
};

export const useGetHotelOfRoomType = (roomTypeId: number) => {
  return useQuery({
    queryKey: ['room-type-hotel', roomTypeId],
    queryFn: () => fetchHotelOfRoomType(roomTypeId),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};
