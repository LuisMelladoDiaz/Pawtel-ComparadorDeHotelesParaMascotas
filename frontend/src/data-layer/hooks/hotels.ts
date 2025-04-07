import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { type MaybeRef, toValue } from 'vue';
import {
  fetchAllHotels,
  fetchHotelById,
  createHotel,
  updateHotel,
  partialUpdateHotel,
  deleteHotel,
  uploadImageToHotel,
  filterAvailableHotels,
  filterAvailableRoomTypes,
  type Hotel,
  fetchRoomTypesByHotel,
} from '@/data-layer/api/hotels';

export const useGetAllHotels = (filters?: Record<string, MaybeRef<any>>) => {
  return useQuery({
    queryKey: ['hotels', filters],
    queryFn: () => fetchAllHotels({
      ...Object.fromEntries(
        Object.entries(filters ?? {})
          .map(([key, value]) => [key, toValue(value)])
          .filter((keyval) => Boolean(keyval[1]))
      ),
    }),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useGetHotelById = (hotelId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['hotelId', hotelId],
    queryFn: () => fetchHotelById(toValue(hotelId)),
    staleTime: 30 * 1000,
    refetchOnWindowFocus: true,
    refetchOnMount: true,
  });
};

export const useCreateHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createHotel,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
      queryClient.invalidateQueries({ queryKey: ['hotelsOfOwner'] });
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
      queryClient.invalidateQueries({ queryKey: ['hotelId'] });
      queryClient.invalidateQueries({ queryKey: ['hotelsOfOwner'] });
      queryClient.invalidateQueries({ queryKey: ['currentHotelOwner'] });
    },
  });
};

export const usePartialUpdateHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ hotelId, partialData }: { hotelId: number; partialData: Partial<Hotel> }) =>
      partialUpdateHotel(hotelId, partialData),

    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['hotelId', data.id] });
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
      queryClient.invalidateQueries({ queryKey: ['hotelId'] });
      queryClient.invalidateQueries({ queryKey: ['hotelsOfOwner'] });
    },
  });
};

export const useGetRoomTypesByHotel = (hotelId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['roomTypes', hotelId],
    queryFn: () => fetchRoomTypesByHotel(toValue(hotelId)),
    staleTime: 30 * 1000,
    refetchOnWindowFocus: true,
    refetchOnMount: true,
  });
};

export const useUploadImageToHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ hotelId, image, isCover }: { hotelId: MaybeRef<number>; image: MaybeRef<File>; isCover: MaybeRef<boolean> }) => {

      return uploadImageToHotel(toValue(hotelId), toValue(image), toValue(isCover));
    },

    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['hotelId', data.id] });
    },
  });
};

export const useFilterAvailableHotels = (filters: Record<string, any>) => {
  return useQuery({
    queryKey: ['available-hotels', filters],
    queryFn: () => filterAvailableHotels(filters),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useFilterAvailableRoomTypes = (hotelId: number, filters: Record<string, any>) => {
  return useQuery({
    queryKey: ['available-room-types', hotelId, filters],
    queryFn: () => filterAvailableRoomTypes(hotelId, filters),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};
