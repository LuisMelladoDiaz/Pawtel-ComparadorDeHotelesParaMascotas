import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type Hotel = {
  id: number;
  name: string;
  address: string;
  city: string;
  description: string;
};

// Obtener todos los hoteles
export const fetchAllHotels = async () => {
  const url = `${API_BASE_URL}/hotels`;
  const response = await axios.get(url);
  return response.data as Hotel[];
};

// Obtener un hotel por ID
export const fetchHotelById = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}`;
  const response = await axios.get(url);
  return response.data as Hotel;
};

// Crear un hotel
export const createHotel = async (hotelData: Omit<Hotel, 'id'>) => {
  const url = `${API_BASE_URL}/hotels`;
  const response = await axios.post(url, hotelData);
  return response.data as Hotel;
};

// Actualizar un hotel
export const updateHotel = async (hotelId: number, hotelData: Omit<Hotel, 'id'>) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}`;
  const response = await axios.put(url, hotelData);
  return response.data as Hotel;
};

// Actualización parcial de un hotel
export const partialUpdateHotel = async (hotelId: number, partialData: Partial<Hotel>) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/`;
  const response = await axios.patch(url, partialData);
  return response.data;
};

// Eliminar un hotel
export const deleteHotel = async (hotelId: number) => {
  const url = `${API_BASE_URL}/hotels/${hotelId}/`;
  const response = await axios.delete(url);
  return response.data;
};
