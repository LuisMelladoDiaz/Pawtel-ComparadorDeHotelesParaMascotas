import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import axios from 'axios';
import { type MaybeRef, toValue } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type Hotel = {
    id: number;
    name: string;
    address: string;
    city: string;
    description: string;
  };

  const fetchAllHotels = async () => {
    const url = `${API_BASE_URL}/hotels`;
    const response = await axios.get(url);
    return response.data as Hotel[];
  };

  export const useGetAllHotels = () => {
    return useQuery({
      queryKey: ['hotels'],
      queryFn: fetchAllHotels,
      staleTime: 1000 * 60,
      refetchOnWindowFocus: false,
    });
  };



const fetchHotelById = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}`;
  const response = await axios.get(url);
  return response.data as Hotel;
}

export const useGetHotelById = (hotelId: MaybeRef<number>) => {
    return useQuery({
        queryKey: ['hotelId', hotelId],
        queryFn: () => fetchHotelById(toValue(hotelId)),
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });

};

const createHotel = async (hotelData: Omit<Hotel, 'id'>) => {
    const url = `${API_BASE_URL}/hotels`;
    const response = await axios.post(url, hotelData);
    return response.data as Hotel;
}

export const useCreateHotel = () => {
    return useMutation({
      mutationFn: createHotel,
      onSuccess: (data) => {
        console.log('Hotel creado con éxito:', data);
      },
      onError: (error) => {
        console.error('Error al crear el hotel:', error);
      },
    });
  };



const updateHotel = async (hotelId: number, hotelData: Omit<Hotel, 'id'>) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}`;
  const response = await axios.put(url, hotelData);
  return response.data as Hotel;
};

export const useUpdateHotel = () => {
  const queryClient = useQueryClient();

  return useMutation({

    mutationFn: ({ hotelId, hotelData }: { hotelId: number; hotelData: Omit<Hotel, 'id'> }) =>
      updateHotel(hotelId, hotelData),

    onSuccess: (data) => {
      console.log('Hotel actualizadio con exito', data);

      queryClient.invalidateQueries({queryKey: ['hotels']});
      queryClient.invalidateQueries({queryKey: ['hotelId', data.id]});

    },

    onError: (error) => {
      console.error('Error al actualizar el hotel:', error);
    },

  });

};


export const partialUpdateHotel = async (hotelId: number, partialData: Partial<Hotel>) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/`;
  const response = await axios.patch(url, partialData);
  return response.data;
};

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


export const deleteHotel = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/`;
  const response = await axios.delete(url);
  return response.data;
};

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
