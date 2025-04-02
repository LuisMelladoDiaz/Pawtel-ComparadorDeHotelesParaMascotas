import { useQuery, useMutation, useQueryClient  } from '@tanstack/vue-query';
import {
  fetchHotelImage,
  fetchAllHotelImages,
  uploadHotelImage,
  updateHotelImage,
  partialUpdateHotelImage,
  deleteHotelImage,
  setCoverImage,
  unsetCoverImage,
  fetchCoverImage,
  fetchNonCoverImages,
} from '@/data-layer/api/hotelImages';

export const useGetHotelImage = (hotelId: number, imageId: number) => {
  return useQuery({
    queryKey: ['hotel-image', hotelId, imageId],
    queryFn: () => fetchHotelImage(hotelId, imageId),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useGetAllHotelImages = (hotelId: number) => {
  return useQuery({
    queryKey: ['hotel-images', hotelId],
    queryFn: () => fetchAllHotelImages(hotelId),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};
export const useUploadHotelImage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ hotelId, image, isCover }: { hotelId: number; image: File; isCover: boolean }) => {
      return await uploadHotelImage(hotelId, image, isCover);
    },
    onSuccess: (_, { hotelId }) => {

      queryClient.invalidateQueries({ queryKey: ['hotelId', hotelId] });
    },
    onError: (error) => {
      console.error('Error al subir imagen:', error);
    },
  });
};

export const useUpdateHotelImage = () => {
  return useMutation({
    mutationFn: (data: { hotelId: number; imageId: number; image: string; isCover: boolean }) =>
      updateHotelImage(data.hotelId, data.imageId, data.image, data.isCover),
  });
};

export const usePartialUpdateHotelImage = () => {
  return useMutation({
    mutationFn: (data: { hotelId: number; imageId: number; image: string; isCover: boolean }) =>
      partialUpdateHotelImage(data.hotelId, data.imageId, data.image, data.isCover),
  });
};

export const useDeleteHotelImage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ hotelId, imageId }: { hotelId: number; imageId: number }) => {
      return await deleteHotelImage(hotelId, imageId);
    },
    onSuccess: (_, { hotelId }) => {
      queryClient.invalidateQueries({ queryKey: ['hotelId', hotelId] });
    },
    onError: (error) => {
      console.error('Error al eliminar imagen:', error);
    },
  });
};


export const useSetCoverImage = () => {
  return useMutation({
    mutationFn: (data: { hotelId: number; imageId: number }) => setCoverImage(data.hotelId, data.imageId),
  });
};

export const useUnsetCoverImage = () => {
  return useMutation({
    mutationFn: (data: { hotelId: number; imageId: number }) => unsetCoverImage(data.hotelId, data.imageId),
  });
};

export const useGetCoverImage = (hotelId: number) => {
  return useQuery({
    queryKey: ['hotel-cover-image', hotelId],
    queryFn: () => fetchCoverImage(hotelId),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};

export const useGetNonCoverImages = (hotelId: number) => {
  return useQuery({
    queryKey: ['hotel-non-cover-images', hotelId],
    queryFn: () => fetchNonCoverImages(hotelId),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};
