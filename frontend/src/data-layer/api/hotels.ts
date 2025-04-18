import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
import { type RoomType } from '@/data-layer/api/roomTypes';
import type { Booking } from './bookings';

export type Hotel = {
  id?: number;
  is_archived: boolean;
  name: string;
  address: string;
  city: string;
  description: string;
  hotel_owner?: string;
  images?: any[];
};


export const fetchAllHotels = async (filters?: Record<string, any>) => {
  const queryParams = new URLSearchParams(filters).toString();
  const url = `${API_BASE_URL}/hotels?${queryParams}`;
  const response = await axios.get(url);
  console.log("api - ",response.data as Hotel[])
  return response.data as Hotel[];
};

export const fetchHotelById = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}`;
  const response = await axios.get(url);
  return response.data as Hotel;
};

export const createHotel = async (hotelData: Omit<Hotel, 'id'>) => {
  const url = `${API_BASE_URL}/hotels/`;
  const response = await axios.post(url, hotelData);
  return response.data as Hotel;
};

export const updateHotel = async (hotelId: number, hotelData: Omit<Hotel, 'id'>) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/`;
  const response = await axios.put(url, hotelData);
  return response.data as Hotel;
};

export const partialUpdateHotel = async (hotelId: number, partialData: Partial<Hotel>) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/`;
  const response = await axios.patch(url, partialData);
  return response.data;
};

export const deleteHotel = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/`;
  const response = await axios.delete(url);
  return response.data;
};

export const fetchRoomTypesByHotel = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/room-types/`;
  const response = await axios.get(url);
  return response.data;
};

export const uploadImageToHotel = async (hotelId: number, image: File, isCover: boolean) => {
  const formData = new FormData();
  formData.append('image', image, image.name);
  formData.append('is_cover', isCover ? 'true' : 'false');
  const response = await axios.post(
    `${API_BASE_URL}/hotels/${hotelId}/upload_image/`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );
  return response.data;
}

export const filterAvailableHotels = async (filters: Record<string, any>) => {
  const url = new URL(`${API_BASE_URL}/hotels/available/`);
  Object.keys(filters).forEach(key => url.searchParams.append(key, filters[key]));
  const response = await axios.get(url.toString());
  return response.data as Hotel[];
};

export const filterAvailableRoomTypes = async (hotelId: number, filters: Record<string, any>) => {
  const url = new URL(`${API_BASE_URL}/hotels/${hotelId}/room-types/available/`);
  Object.keys(filters).forEach(key => url.searchParams.append(key, filters[key]));
  const response = await axios.get(url.toString());
  return response.data as RoomType[];
};

export const fetchBookingsByHotel = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/bookings`;
  const response = await axios.get(url);
  return response.data as Booking[];
};
