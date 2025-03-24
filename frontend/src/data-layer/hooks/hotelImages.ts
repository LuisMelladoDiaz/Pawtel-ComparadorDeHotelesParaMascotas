import { useQuery, useMutation } from '@tanstack/vue-query';
import { ref } from 'vue';
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
  return useMutation({
    mutationFn: (data: { hotelId: number; image: File; isCover: boolean }) =>
      uploadHotelImage(data.hotelId, data.image, data.isCover),
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
  return useMutation({
    mutationFn: (data: { hotelId: number; imageId: number }) => deleteHotelImage(data.hotelId, data.imageId),
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
