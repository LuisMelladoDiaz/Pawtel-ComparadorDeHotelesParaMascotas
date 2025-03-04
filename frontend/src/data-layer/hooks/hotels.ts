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

// Obtener todos los hoteles
export const useGetAllHotels = () => {
  return useQuery({
    queryKey: ['hotels'],
    queryFn: fetchAllHotels,
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false
  });
};

// Obtener un hotel por ID
export const useGetHotelById = (hotelId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['hotelId', hotelId],
    queryFn: () => fetchHotelById(toValue(hotelId)),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

// Crear un hotel
export const useCreateHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createHotel,
    onSuccess: (data) => {
      console.log('Hotel creado con éxito:', data);
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
    },
    onError: (error) => {
      console.error('Error al crear el hotel:', error);
    },
  });
};

// Actualizar un hotel
export const useUpdateHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ hotelId, hotelData }: { hotelId: number; hotelData: Omit<Hotel, 'id'> }) =>
      updateHotel(hotelId, hotelData),

    onSuccess: (data: Hotel) => {
      console.log('Hotel actualizado con éxito', data);
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
      queryClient.invalidateQueries({ queryKey: ['hotelId', data.id] });
    },

    onError: (error) => {
      console.error('Error al actualizar el hotel:', error);
    },
  });
};

// Actualización parcial de un hotel
export const usePartialUpdateHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ hotelId, partialData }: { hotelId: number; partialData: Partial<Hotel> }) =>
      partialUpdateHotel(hotelId, partialData),

    onSuccess: (data) => {
      console.log('Hotel actualizado parcialmente:', data);
      queryClient.invalidateQueries({ queryKey: ['hotel', data.id] });
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
    },
  });
};

// Eliminar un hotel
export const useDeleteHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteHotel,

    onSuccess: () => {
      console.log('Hotel eliminado con éxito');
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
    },
  });
};
