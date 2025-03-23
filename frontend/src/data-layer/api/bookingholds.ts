import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type BookingHold = {
    id: number;
    hold_expires_at: string;
    booking_start_date: string;
    booking_end_date: string;
    customer: number;
    room_type: number;
    is_expired: boolean;
};

export const fetchBookingHoldById = async (id: number): Promise<BookingHold> => {
    const url = `${API_BASE_URL}/booking-holds/${id}/`;
    const response = await axios.get(url);
    return response.data as BookingHold;
};

export const fetchAllBookingHolds = async (): Promise<BookingHold[]> => {
    const url = `${API_BASE_URL}/booking-holds/`;
    const response = await axios.get(url);
    return response.data as BookingHold[];
};

export const createBookingHold = async (data: Omit<BookingHold, 'id' | 'is_expired'>): Promise<BookingHold> => {
    const url = `${API_BASE_URL}/booking-holds/`;
    const response = await axios.post(url, data);
    return response.data as BookingHold;
};

export const deleteBookingHold = async (id: number): Promise<void> => {
    const url = `${API_BASE_URL}/booking-holds/${id}/`;
    await axios.delete(url);
};
