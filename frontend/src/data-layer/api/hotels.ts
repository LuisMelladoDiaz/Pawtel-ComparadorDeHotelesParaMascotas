import api from "@/api";
import { type RoomType } from "@/data-layer/api/roomTypes";
import type { Booking } from "./bookings";

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
  const url = `hotels?${queryParams}`;
  const response = await api.get(url);
  return response.json<Hotel[]>();
};

export const fetchHotelById = async (hotelId: number) => {
  const url = `hotels/${hotelId}`;
  const response = await api.get(url);
  return await response.json<Hotel>();
};

export const createHotel = async (hotelData: Omit<Hotel, "id">) => {
  const url = `hotels/`;
  const response = await api.post(url, { json: hotelData });
  return await response.json<Hotel>();
};

export const updateHotel = async (hotelId: number, hotelData: Omit<Hotel, "id">) => {
  const url = `hotels/${hotelId}/`;
  const response = await api.put(url, { json: hotelData });
  return await response.json<Hotel>();
};

export const partialUpdateHotel = async (hotelId: number, partialData: Partial<Hotel>) => {
  const url = `hotels/${hotelId}/`;
  const response = await api.patch(url, { json: partialData });
  return await response.json();
};

export const deleteHotel = async (hotelId: number) => {
  const url = `hotels/${hotelId}/`;
  await api.delete(url);
};

export const fetchRoomTypesByHotel = async (hotelId: number) => {
  const url = `hotels/${hotelId}/room-types/`;
  const response = await api.get(url);
  return await response.json<RoomType[]>();
};

export const uploadImageToHotel = async (hotelId: number, image: File, isCover: boolean) => {
  const formData = new FormData();
  formData.append("image", image, image.name);
  formData.append("is_cover", isCover ? "true" : "false");
  const url = `hotels/${hotelId}/upload_image/`;
  const response = await api.post(url, { body: formData });
  return await response.json();
};

export const filterAvailableHotels = async (filters: Record<string, any>) => {
  const url = new URL(`hotels/available/`, window.location.origin);
  Object.keys(filters).forEach((key) => url.searchParams.append(key, filters[key]));
  const response = await api.get(url.pathname + url.search);
  return await response.json<Hotel[]>();
};

export const filterAvailableRoomTypes = async (hotelId: number, filters: Record<string, any>) => {
  const url = new URL(`hotels/${hotelId}/room-types/available/`, window.location.origin);
  Object.keys(filters).forEach((key) => url.searchParams.append(key, filters[key]));
  const response = await api.get(url.pathname + url.search);
  return await response.json<RoomType[]>();
};

export const fetchBookingsByHotel = async (hotelId: number) => {
  const url = `hotels/${hotelId}/bookings`;
  const response = await api.get(url);
  return await response.json<Booking[]>();
};
