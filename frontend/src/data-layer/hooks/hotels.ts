import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { type MaybeRef, toValue } from 'vue';
import {
  fetchAllHotels,
  fetchHotelById,
  createHotel,
  updateHotel,
  partialUpdateHotel,
  deleteHotel,
  type Hotel,
} from '@/data-layer/api/hotels';

export const useGetAllHotels = (filters?: Record<string, MaybeRef<any>>) => {
  return useQuery({
    queryKey: ['hotels', filters],
    queryFn: () => fetchAllHotels({
      ...Object.fromEntries(Object.entries(filters || {}).map(([key, value]) => [key, toValue(value)])),
    }),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useGetHotelById = (hotelId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['hotelId', hotelId],
    queryFn: () => fetchHotelById(toValue(hotelId)),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useCreateHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createHotel,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
    },
  });
};

export const useUpdateHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ hotelId, hotelData }: { hotelId: number; hotelData: Omit<Hotel, 'id'> }) =>
      updateHotel(hotelId, hotelData),

    onSuccess: (data: Hotel) => {
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
      queryClient.invalidateQueries({ queryKey: ['hotelId', data.id] });
    },
  });
};

export const usePartialUpdateHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ hotelId, partialData }: { hotelId: number; partialData: Partial<Hotel> }) =>
      partialUpdateHotel(hotelId, partialData),

    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['hotel', data.id] });
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
    },
  });
};

export const useDeleteHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteHotel,

    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
    },
  });
};
