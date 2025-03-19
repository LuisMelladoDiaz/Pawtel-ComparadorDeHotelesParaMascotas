import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type Booking = {
  id?: number;
  customer_id: number;
  room_type_id: number;
  start_date: string;
  end_date: string;
  total_price: number;
};

export const fetchAllBookings = async () => {
  const url = `${API_BASE_URL}/bookings/`;
  const response = await axios.get(url);
  return response.data as Booking[];
};

export const fetchBookingById = async (bookingId: number) => {
  const url = `${API_BASE_URL}/bookings/${bookingId}/`;
  const response = await axios.get(url);
  return response.data as Booking;
};