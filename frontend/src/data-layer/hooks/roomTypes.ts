import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { type MaybeRef, toValue } from 'vue';
import {
  fetchAllRoomTypes,
  fetchRoomTypeById,
  createRoomType,
  updateRoomType,
  partialUpdateRoomType,
  deleteRoomType,
  checkRoomTypeAvailability,
  fetchHotelOfRoomType,
  fetchTotalVacancyForRoomType,
  fetchVacancyForEachRoomInRoomType,
  fetchRoomTypesByIds,
  type RoomType,
} from '@/data-layer/api/roomTypes';

export const useGetRoomTypeById = (roomTypeId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomType', roomTypeId],
    queryFn: () => fetchRoomTypeById(toValue(roomTypeId)),
    staleTime: 30 * 1000,
    refetchOnWindowFocus: true,
    refetchOnMount: true,
  });
};

export const useGetRoomTypesByIds = (roomTypeIds: MaybeRef<number[]>, opts) => {
  return useQuery({
    queryKey: ['roomTypeIds', roomTypeIds],
    queryFn: () => fetchRoomTypesByIds(toValue(roomTypeIds)),
    staleTime: 30 * 1000,
    refetchOnWindowFocus: true,
    refetchOnMount: true,
    enabled: opts?.enabled,
  });
};

export const useGetAllRoomTypes = (hotelId?: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomTypes', hotelId],
    queryFn: () => fetchAllRoomTypes(toValue(hotelId)),
    staleTime: 30 * 1000,
    refetchOnWindowFocus: true,
    refetchOnMount: true,
  });
};

export const useCreateRoomType = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Omit<RoomType, 'id'>) => createRoomType(data),

    onSuccess: (data: RoomType, variables) => {
      // Invalidar consultas de tipos de habitación
      queryClient.invalidateQueries({ queryKey: ['roomTypes'] });

      // Invalidar consultas relacionadas con el hotel
      const hotelId = variables.hotel;
      if (hotelId) {
        queryClient.invalidateQueries({ queryKey: ['roomTypes', hotelId] });
        queryClient.invalidateQueries({ queryKey: ['hotelId', hotelId] });
        queryClient.invalidateQueries({ queryKey: ['hotels'] });
      }
    },
  });
};

export const useUpdateRoomType = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ roomTypeId, roomTypeData }: { roomTypeId: number; roomTypeData: Omit<RoomType, 'id'> }) =>
      updateRoomType(roomTypeId, roomTypeData),

    onSuccess: (data: RoomType, variables) => {
      // Invalidar consultas de tipos de habitación
      queryClient.invalidateQueries({ queryKey: ['roomTypes'] });
      queryClient.invalidateQueries({ queryKey: ['roomType', data.id] });

      // Invalidar consultas relacionadas con el hotel
      const hotelId = variables.roomTypeData.hotel;
      if (hotelId) {
        queryClient.invalidateQueries({ queryKey: ['roomTypes', hotelId] });
        queryClient.invalidateQueries({ queryKey: ['hotelId', hotelId] });
        queryClient.invalidateQueries({ queryKey: ['hotels'] });
      }
    },
  });
};

export const usePartialUpdateRoomType = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ roomTypeId, partialData }: { roomTypeId: number; partialData: Partial<RoomType> }) =>
      partialUpdateRoomType(roomTypeId, partialData),

    onSuccess: (data: RoomType) => {
      queryClient.invalidateQueries({ queryKey: ['roomType', data.id] });
      queryClient.invalidateQueries({ queryKey: ['roomTypes'] });
    },
  });
};

export const useDeleteRoomType = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteRoomType,

    onSuccess: (_, roomTypeId) => {
      // Invalidar todas las consultas de tipos de habitación
      queryClient.invalidateQueries({ queryKey: ['roomTypes'] });
      queryClient.invalidateQueries({ queryKey: ['roomType', roomTypeId] });

      // Invalidar consultas de hoteles (ya que no tenemos el hotelId específico)
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
    },
  });
};

export const useCheckRoomTypeAvailability = () => {
  return useMutation({
    mutationFn: (data: { roomTypeId: number; startDate: string; endDate: string }) =>
      checkRoomTypeAvailability(data.roomTypeId, data.startDate, data.endDate),
  });
};

export const useGetHotelOfRoomType = (roomTypeId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomTypeHotel', roomTypeId],
    queryFn: () => fetchHotelOfRoomType(toValue(roomTypeId)),
    staleTime: 30 * 1000,
    refetchOnWindowFocus: true,
    refetchOnMount: true,
  });
};

export const useGetTotalVacancyForRoomType = (roomTypeId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomTypeVacancy', roomTypeId],
    queryFn: () => fetchTotalVacancyForRoomType(toValue(roomTypeId)),
    staleTime: 30 * 1000,
    refetchOnWindowFocus: true,
    refetchOnMount: true,
  });
};

export const useGetVacancyForEachRoomInRoomType = (roomTypeId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomTypeRoomVacancy', roomTypeId],
    queryFn: () => fetchVacancyForEachRoomInRoomType(toValue(roomTypeId)),
    staleTime: 30 * 1000,
    refetchOnWindowFocus: true,
    refetchOnMount: true,
  });
};
