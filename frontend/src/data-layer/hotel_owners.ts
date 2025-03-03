import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import axios from 'axios';
import { type MaybeRef, toValue } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type Hotel_Owner = {
    id: number;
    phone: number;
    email: string;
  };
type Hotel = {
    id: number;
    name: string;
    address: string;
    city: string;
    description: string;
  };

  const fetchAllOwners = async () => {
    const url = `${API_BASE_URL}/api/hotel-owners/`;
    const response = await axios.get(url);
    return response.data as Hotel_Owner[];
  };

  export const useGetAllHotelOwners = () => {
    return useQuery({
      queryKey: ['hotelOwners'],
      queryFn: fetchAllOwners,
      staleTime: 1000 * 60,
      refetchOnWindowFocus: false,
    });
  };



const fetchHotelOwnerById = async (hotelOwnerId: number) => {
  const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}`;
  const response = await axios.get(url);
  return response.data as Hotel_Owner;
}

export const useGetHotelOwnerById = (hotelOwnerId: MaybeRef<number>) => {
    return useQuery({
        queryKey: ['hotelOwnerId', hotelOwnerId],
        queryFn: () => fetchHotelOwnerById(toValue(hotelOwnerId)),
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });

};

const createHotelOwner = async (hotelOwnerData: Omit<Hotel_Owner, 'id'>) => {
    const url = `${API_BASE_URL}/hotel-owners/`;
    const response = await axios.post(url, hotelOwnerData);
    return response.data as Hotel_Owner;
}

export const useCreateHotelOwner = () => {
    return useMutation({
      mutationFn: createHotelOwner,
      onSuccess: (data) => {
        console.log('Dueño de hotel creado con éxito:', data);
      },
      onError: (error) => {
        console.error('Error al crear el dueño de hotel:', error);
      },
    });
  };

export const updateHotelOwner = async (hotelOwnerId: number, ownerData: HotelOwner) => {
  const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/`;
  const response = await axios.put(url, ownerData);
  return response.data as Hotel_Owner;
};


export const useUpdateHotelOwner = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ hotelOwnerId, ownerData }: { hotelOwnerId: number; ownerData: HotelOwner }) =>
      updateHotelOwner(hotelOwnerId, ownerData),

    onSuccess: (data) => {
      console.log('Dueño de hotel actualizado:', data);
      queryClient.invalidateQueries({ queryKey: ['hotelOwner', data.id] });
    },
  });
};

export const partialUpdateHotelOwner = async (hotelOwnerId: number, partialData: Partial<HotelOwner>) => {
  const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/`;
  const response = await axios.patch(url, partialData);
  return response.data;
};

export const usePartialUpdateHotelOwner = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ hotelOwnerId, partialData }: { hotelOwnerId: number; partialData: Partial<HotelOwner> }) =>
      partialUpdateHotelOwner(hotelOwnerId, partialData),

    onSuccess: (data) => {
      console.log('Dueño de hotel actualizado parcialmente:', data);
      queryClient.invalidateQueries({ queryKey: ['hotelOwner', data.id] });
    },
  });
};

export const deleteHotelOwner = async (hotelOwnerId: number) => {
  const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/`;
  const response = await axios.delete(url);
  return response.data;
};

export const useDeleteHotelOwner = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteHotelOwner,

    onSuccess: () => {
      console.log('Dueño de hotel eliminado');
      queryClient.invalidateQueries({ queryKey: ['hotelOwners'] });
    },
  });
};

export const fetchAllHotelsOfOwner = async (hotelOwnerId: number) => {
  const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/hotels/`;
  const response = await axios.get(url);
  return response.data as Hotel[];
};


export const useGetAllHotelsOfOwner = (hotelOwnerId: number) => {
  return useQuery({
    queryKey: ['hotelsOfOwner', hotelOwnerId],
    queryFn: () => fetchAllHotelsOfOwner(hotelOwnerId),
    enabled: !!hotelOwnerId,
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const deleteAllHotelsOfOwner = async (hotelOwnerId: number) => {
  const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/hotels/`;
  const response = await axios.delete(url);
  return response.data;
};

export const useDeleteAllHotelsOfOwner = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteAllHotelsOfOwner,

    onSuccess: () => {
      console.log('Todos los hoteles del dueño eliminados');
      queryClient.invalidateQueries({ queryKey: ['hotels'] });
      queryClient.invalidateQueries({ queryKey: ['hotelOwner'] });
    },
  });
};
