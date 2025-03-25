import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type HotelImage = {
  id?: number;
  image: string;
  is_cover: boolean;
  hotel: number;
};

export const fetchHotelImage = async (hotelId: number, imageId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/hotel-images/${imageId}/`;
  const response = await axios.get(url);
  return response.data as HotelImage;
};

export const fetchAllHotelImages = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/hotel-images/all/`;
  const response = await axios.get(url);
  return response.data as HotelImage[];
};

export const uploadHotelImage = async (hotelId: number, image: File, isCover: boolean) => {
  const formData = new FormData();
  formData.append('image', image, image.name);
  formData.append('is_cover', isCover ? 'true' : 'false');

  const url = `${API_BASE_URL}/hotels/${hotelId}/hotel-images/upload/`;
  const response = await axios.post(url, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });

  return response.data as HotelImage;
};

export const updateHotelImage = async (hotelId: number, imageId: number, image: string, isCover: boolean) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/hotel-images/${imageId}/update/`;
  const response = await axios.put(url, { image, is_cover: isCover });
  return response.data as HotelImage;
};

export const partialUpdateHotelImage = async (hotelId: number, imageId: number, image: string, isCover: boolean) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/hotel-images/${imageId}/patch/`;
  const response = await axios.patch(url, { image, is_cover: isCover });
  return response.data as HotelImage;
};

export const deleteHotelImage = async (hotelId: number, imageId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/hotel-images/${imageId}/delete/`;
  const response = await axios.delete(url);
  return response.data;
};

export const setCoverImage = async (hotelId: number, imageId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/hotel-images/${imageId}/set-cover/`;
  const response = await axios.put(url);
  return response.data as HotelImage;
};

export const unsetCoverImage = async (hotelId: number, imageId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/hotel-images/${imageId}/set-non-cover/`;
  const response = await axios.put(url);
  return response.data as HotelImage;
};

export const fetchCoverImage = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/hotel-images/cover/`;
  const response = await axios.get(url);
  return response.data as HotelImage;
};

export const fetchNonCoverImages = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/hotel-images/non-cover/`;
  const response = await axios.get(url);
  return response.data as HotelImage[];
};
