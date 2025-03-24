import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { type MaybeRef, toValue } from 'vue';
import {
  fetchAllRoomTypes,
  fetchRoomTypeById,
  createRoomType,
  updateRoomType,
  partialUpdateRoomType,
  deleteRoomType,
  fetchTotalVacancyForRoomType,
  fetchVacancyForEachRoomInRoomType,
  type RoomType,
} from '@/data-layer/api/roomTypes';

export const useGetAllRoomTypes = (hotelId?: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomTypes', hotelId],
    queryFn: () => fetchAllRoomTypes(toValue(hotelId)),
    staleTime: 1000 * 60, // Los datos se mantienen frescos por 1 minuto
    refetchOnWindowFocus: false, // No refrescar los datos cuando la ventana vuelve al foco
  });
};

export const useGetRoomTypeById = (roomTypeId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomTypeId', roomTypeId],
    queryFn: () => fetchRoomTypeById(toValue(roomTypeId)),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useCreateRoomType = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createRoomType,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['roomTypes'] });
    },
  });
};

export const useUpdateRoomType = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ roomTypeId, roomTypeData }: { roomTypeId: number; roomTypeData: Omit<RoomType, 'id'> }) =>
      updateRoomType(roomTypeId, roomTypeData),

    onSuccess: (data: RoomType) => {
      queryClient.invalidateQueries({ queryKey: ['roomTypes'] });
      queryClient.invalidateQueries({ queryKey: ['roomTypeId', data.id] });
    },
  });
};

export const usePartialUpdateRoomType = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ roomTypeId, partialData }: { roomTypeId: number; partialData: Partial<RoomType> }) =>
      partialUpdateRoomType(roomTypeId, partialData),

    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['roomType', data.id] });
      queryClient.invalidateQueries({ queryKey: ['roomTypes'] });
    },
  });
};

export const useDeleteRoomType = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteRoomType,

    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['roomTypes'] });
    },
  });
};

export const useGetTotalVacancyForRoomType = (roomTypeId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomTypeVacancy', roomTypeId],
    queryFn: () => fetchTotalVacancyForRoomType(toValue(roomTypeId)),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useGetAllRoomsForRoomType = (roomTypeId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomTypeRooms', roomTypeId],
    queryFn: () => fetchAllRoomsForRoomType(toValue(roomTypeId)),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useGetVacancyForEachRoomInRoomType = (roomTypeId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomTypeRoomVacancy', roomTypeId],
    queryFn: () => fetchVacancyForEachRoomInRoomType(toValue(roomTypeId)),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};