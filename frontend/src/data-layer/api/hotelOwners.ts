import axios from 'axios';
import { type Hotel } from '@/data-layer/api/hotels';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

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
    const url = `${API_BASE_URL}/hotel-owners/`;
    const response = await axios.get(url);
    return response.data as HotelOwner[];
};

export const fetchHotelOwnerById = async (hotelOwnerId: number) => {
    const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}`;
    const response = await axios.get(url);
    return response.data as HotelOwner;
};

export const createHotelOwner = async (hotelOwnerData: Omit<HotelOwner, 'id'>) => {
    const url = `${API_BASE_URL}/auth/register/`;
    try {
        const response = await axios.post(url, {...hotelOwnerData, role: "hotel_owner"});
        return response.data as HotelOwner;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error("Error en la solicitud:", error.response?.data);
            throw error;
        }
        console.error("Error desconocido:", error);
        throw error;
    }
};

export const updateHotelOwner = async (hotelOwnerId: number, ownerData: HotelOwner) => {
    const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/`;
    const response = await axios.patch(url, ownerData);
    return response.data as HotelOwner;
};

export const partialUpdateHotelOwner = async (hotelOwnerId: number, partialData: Partial<HotelOwner>) => {
    const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/`;
    const response = await axios.patch(url, partialData);
    return response.data;
};

export const deleteHotelOwner = async (hotelOwnerId: number) => {
    const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/`;
    const response = await axios.delete(url);
    return response.data;
};

export const fetchAllHotelsOfOwner = async (hotelOwnerId: number) => {
    const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/hotels/`;
    const response = await axios.get(url);
    return response.data as Hotel[];
};

export const deleteAllHotelsOfOwner = async (hotelOwnerId: number) => {
    const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/hotels/delete/`;
    const response = await axios.delete(url);
    return response.data;
};

export const getCurrentHotelOwner = async () => {
    const url = `${API_BASE_URL}/hotel-owners/me`;
    const response = await axios.get(url);
    return response.data as HotelOwner;
}

export const approveHotelOwner = async (hotelOwnerId: number) => {
    const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/approve/`;
    const response = await axios.patch(url);
    return response.data;
}
