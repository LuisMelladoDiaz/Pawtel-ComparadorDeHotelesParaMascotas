import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type Booking = {
    id: number;
    creation_date: string;
    start_date: string;
    end_date: string;
    total_price: string; // we keep it as string to avoid floating point issues
    customer: number;
    room_type: number;
};

export const fetchBookingById = async (id: number): Promise<Booking> => {
    const url = `${API_BASE_URL}/bookings/${id}/`;
    const response = await axios.get(url);
    return response.data as Booking;
};

export const fetchAllBookings = async (): Promise<Booking[]> => {
    const url = `${API_BASE_URL}/bookings/`;
    const response = await axios.get(url);
    return response.data as Booking[];
};
