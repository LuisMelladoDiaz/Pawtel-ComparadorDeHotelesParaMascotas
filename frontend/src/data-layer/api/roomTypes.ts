import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type RoomType = {
  id?: number;
  name: string;
  description: string;
  capacity: number;
  num_rooms: number;
  price_per_night: number;
  pet_type: string;
  hotel: number; // hotel ID
  is_archived: boolean;
};

export const fetchRoomTypeById = async (roomTypeId: number) => {
  const url = `${API_BASE_URL}/room-types/${roomTypeId}/`;
  const response = await axios.get(url);
  return response.data as RoomType;
};

export const fetchAllRoomTypes = async (hotelId?: number) => {
  const url = hotelId ? `${API_BASE_URL}/hotels/${hotelId}/room-types/` : `${API_BASE_URL}/room-types/`;
  const response = await axios.get(url);
  return response.data as RoomType[];
};

export const createRoomType = async (roomTypeData: Omit<RoomType, 'id'>) => {
  const url = `${API_BASE_URL}/room-types/`;
  const response = await axios.post(url, roomTypeData);
  return response.data as RoomType;
};

export const updateRoomType = async (roomTypeId: number, roomTypeData: Omit<RoomType, 'id'>) => {
  const url = `${API_BASE_URL}/room-types/${roomTypeId}/`;
  const response = await axios.put(url, roomTypeData);
  return response.data as RoomType;
};

export const partialUpdateRoomType = async (roomTypeId: number, partialData: Partial<RoomType>) => {
  const url = `${API_BASE_URL}/room-types/${roomTypeId}/`;
  const response = await axios.patch(url, partialData);
  return response.data as RoomType;
};

export const deleteRoomType = async (roomTypeId: number) => {
  const url = `${API_BASE_URL}/room-types/${roomTypeId}/`;
  const response = await axios.delete(url);
  return response.data;
};

export const checkRoomTypeAvailability = async (roomTypeId: number, startDate: string, endDate: string) => {
  const url = `${API_BASE_URL}/room-types/${roomTypeId}/is-available?start_date=${startDate}&end_date=${endDate}`;
  const response = await axios.get(url);
  return response.data;
};

export const fetchHotelOfRoomType = async (roomTypeId: number) => {
  const url = `${API_BASE_URL}/room-types/${roomTypeId}/hotel`;
  const response = await axios.get(url);
  return response.data;
};

export const fetchTotalVacancyForRoomType = async (roomTypeId: number) => {
  const url = `${API_BASE_URL}/room-types/${roomTypeId}/total-vacancy/`;
  const response = await axios.get(url);
  return response.data as { id: number; total_vacancy: number };
};

export const fetchVacancyForEachRoomInRoomType = async (roomTypeId: number) => {
  const url = `${API_BASE_URL}/room-types/${roomTypeId}/rooms/vacancy/`;
  const response = await axios.get(url);
  return response.data as { room_id: number; vacancy: number }[];
};
