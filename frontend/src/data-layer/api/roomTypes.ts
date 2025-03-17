import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type RoomType = {
  id?: number;
  is_archived: boolean;
  name: string;
  description: string;
  capacity: number;
  price_per_night: number;
  pet_type: string;
  hotel?: number; // ID del hotel al que pertenece
};

export const fetchAllRoomTypes = async (hotelId?: number) => {
  const url = hotelId ? `${API_BASE_URL}/hotels/${hotelId}/room-types/` : `${API_BASE_URL}/room-type/`;
  const response = await axios.get(url);
  return response.data as RoomType[];
};

export const fetchRoomTypeById = async (roomTypeId: number) => {
  const url = `${API_BASE_URL}/room-type/${roomTypeId}/`;
  const response = await axios.get(url);
  return response.data as RoomType;
};

export const createRoomType = async (roomTypeData: Omit<RoomType, 'id'>) => {
  const url = `${API_BASE_URL}/room-type/`;
  const response = await axios.post(url, roomTypeData);
  return response.data as RoomType;
};

export const updateRoomType = async (roomTypeId: number, roomTypeData: Omit<RoomType, 'id'>) => {
  const url = `${API_BASE_URL}/room-type/${roomTypeId}/`;
  const response = await axios.put(url, roomTypeData);
  return response.data as RoomType;
};

export const partialUpdateRoomType = async (roomTypeId: number, partialData: Partial<RoomType>) => {
  const url = `${API_BASE_URL}/room-type/${roomTypeId}/`;
  const response = await axios.patch(url, partialData);
  return response.data;
};

export const deleteRoomType = async (roomTypeId: number) => {
  const url = `${API_BASE_URL}/room-type/${roomTypeId}/`;
  const response = await axios.delete(url);
  return response.data;
};

export const fetchTotalVacancyForRoomType = async (roomTypeId: number) => {
  const url = `${API_BASE_URL}/room-type/${roomTypeId}/total-vacancy/`;
  const response = await axios.get(url);
  return response.data as { id: number, total_vacancy: number };
};


export const fetchVacancyForEachRoomInRoomType = async (roomTypeId: number) => {
  const url = `${API_BASE_URL}/room-type/${roomTypeId}/rooms/vacancy/`;
  const response = await axios.get(url);
  return response.data as { room_id: number, vacancy: number }[];
};