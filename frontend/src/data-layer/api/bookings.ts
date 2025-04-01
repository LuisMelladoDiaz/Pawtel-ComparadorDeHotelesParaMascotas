import axios from 'axios';
import { useRouter } from 'vue-router';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

export type Booking = {
  id?: number;
  creation_date?: string;
  start_date: string;
  end_date: string;
  total_price: number;
  customer?: number;
  customer_id?: number;
  room_type?: number;
  room_type_id?: number;
  hotel_id?: number;
};

export const createBooking = async (BookingData: Omit<Booking, 'id'>) => {
  const url = `${API_BASE_URL}/bookings/`;
  try {
    const response = await axios.post(url, { ...BookingData, role: "customer" });

    if (response.data?.url) {
      window.location.href = response.data.url; // Redirect to Stripe
    }

    return response.data as string;
  } catch (error) {
    if (axios.isAxiosError(error)) {
        console.error("Error en la solicitud:", error.response?.data);
        throw error;
    }
    console.error("Error desconocido:", error);
    throw error;
}
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
