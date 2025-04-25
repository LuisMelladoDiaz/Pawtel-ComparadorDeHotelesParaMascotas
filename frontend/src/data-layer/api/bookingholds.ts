import api from "@/api";

export type BookingHold = {
    id?: number;
    hold_expires_at: string;
    booking_start_date: string;
    booking_end_date: string;
    customer: number;
    room_type: number;
    is_expired: boolean;
};

export const fetchBookingHoldById = async (id: number): Promise<BookingHold> => {
    const url = `booking-holds/${id}/`;
    const response = await api.get(url);
    return await response.json<BookingHold>();
};

export const fetchAllBookingHolds = async (): Promise<BookingHold[]> => {
    const url = `booking-holds/`;
    const response = await api.get(url);
    return await response.json<BookingHold[]>();
};

export const createBookingHold = async (data: Omit<BookingHold, "id" | "is_expired">): Promise<BookingHold> => {
    const url = `booking-holds/`;
    const response = await api.post(url, { json: data });
    return await response.json<BookingHold>();
};

export const deleteBookingHold = async (id: number): Promise<void> => {
    const url = `booking-holds/${id}/`;
    await api.delete(url);
}
