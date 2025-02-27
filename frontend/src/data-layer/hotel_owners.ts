import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import axios from 'axios';
import { type MaybeRef, toValue } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type Hotel_Owner = {
    id: number;
    name: string;
    description: string;
    location: string;
    rating: number;
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
