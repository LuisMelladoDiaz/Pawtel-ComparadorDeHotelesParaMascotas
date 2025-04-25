import api from "@/api";
import { type Hotel } from "@/data-layer/api/hotels";

export type HotelOwner = {
    id?: number;
    username: string;
    email: string;
    phone: string;
    password: string;
    date_joined?: string;
    last_login?: string;
    is_active?: boolean;
    is_approved?: boolean;
};

export const fetchAllOwners = async () => {
    const url = `hotel-owners/`;
    const response = await api.get(url);
    return await response.json<HotelOwner[]>();
};

export const fetchHotelOwnerById = async (hotelOwnerId: number) => {
    const url = `hotel-owners/${hotelOwnerId}`;
    const response = await api.get(url);
    return await response.json<HotelOwner>();
};

export const createHotelOwner = async (hotelOwnerData: Omit<HotelOwner, "id">) => {
    const url = `auth/register/`;
    try {
        const response = await api.post(url, { json: { ...hotelOwnerData, role: "hotel_owner" } });
        return await response.json<HotelOwner>();
    } catch (error) {
        console.error(error);
        throw error;
    }
};

export const updateHotelOwner = async (hotelOwnerId: number, ownerData: HotelOwner) => {
    const url = `hotel-owners/${hotelOwnerId}/`;
    const response = await api.patch(url, { json: ownerData });
    return await response.json<HotelOwner>();
};

export const partialUpdateHotelOwner = async (hotelOwnerId: number, partialData: Partial<HotelOwner>) => {
    const url = `hotel-owners/${hotelOwnerId}/`;
    const response = await api.patch(url, { json: partialData });
    return await response.json();
};

export const deleteHotelOwner = async (hotelOwnerId: number) => {
    const url = `hotel-owners/${hotelOwnerId}/`;
    const response = await api.delete(url);
    return await response.json();
};

export const fetchAllHotelsOfOwner = async (hotelOwnerId: number) => {
    const url = `hotel-owners/${hotelOwnerId}/hotels/`;
    const response = await api.get(url);
    return await response.json<Hotel[]>();
};

export const deleteAllHotelsOfOwner = async (hotelOwnerId: number) => {
    const url = `hotel-owners/${hotelOwnerId}/hotels/delete/`;
    const response = await api.delete(url);
    return await response.json();
};

export const getCurrentHotelOwner = async () => {
    const url = `hotel-owners/me`;
    const response = await api.get(url);
    return await response.json<HotelOwner>();
};

export const approveHotelOwner = async (hotelOwnerId: number) => {
    const url = `hotel-owners/${hotelOwnerId}/approve/`;
    const response = await api.patch(url);
    return await response.json();
};
