import { useQuery } from '@tanstack/vue-query';
import axios from 'axios';
import { type MaybeRef, toValue } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type Pet = {
  id: number;
  name: string;
  species: string;
  image: string;
};

const fetchRandomPets = async (count?: number) => {
  const url = count ? `${API_BASE_URL}/random-pets?count=${count}` : `${API_BASE_URL}/random-pets`;
  const response = await axios.get(url);
  return response.data as Pet[];
};

export const useGetRandomPets = (count: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['random-pets', count],
    queryFn: () => fetchRandomPets(toValue(count)),
    staleTime: 1000 * 60, // 1 minute
    refetchOnWindowFocus: false,
  });
};