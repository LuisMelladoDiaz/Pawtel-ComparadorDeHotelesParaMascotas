import api from "@/api";
import { useRouter } from "vue-router";

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

export const createBooking = async (BookingData: Omit<Booking, "id">) => {
  const url = `bookings/`;
  try {
    const response = await api.post(url, { json: { ...BookingData, role: "customer" } }).json<{ url?: string }>();

    if (response?.url) {
      window.location.href = response.url;
    }

    return response.url as string;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const fetchAllBookings = async () => {
  const url = `bookings/`;
  const response = await api.get(url);
  return await response.json<Booking[]>();
};

export const fetchBookingById = async (bookingId: number) => {
  const url = `bookings/${bookingId}/`;
  const response = await api.get(url);
  return await response.json<Booking>();
};
