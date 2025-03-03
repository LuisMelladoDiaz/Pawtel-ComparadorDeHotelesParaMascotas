import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

type Hotel_Owner = {
    id: number;
    phone: number;
    email: string;
};

type Hotel = {
    id: number;
    name: string;
    address: string;
    city: string;
    description: string;
};

export const fetchAllOwners = async () => {
    const url = `${API_BASE_URL}/api/hotel-owners/`;
    const response = await axios.get(url);
    return response.data as Hotel_Owner[];
};

export const fetchHotelOwnerById = async (hotelOwnerId: number) => {
    const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}`;
    const response = await axios.get(url);
    return response.data as Hotel_Owner;
};

export const createHotelOwner = async (hotelOwnerData: Omit<Hotel_Owner, 'id'>) => {
    const url = `${API_BASE_URL}/hotel-owners/`;
    const response = await axios.post(url, hotelOwnerData);
    return response.data as Hotel_Owner;
};

export const updateHotelOwner = async (hotelOwnerId: number, ownerData: Hotel_Owner) => {
    const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/`;
    const response = await axios.put(url, ownerData);
    return response.data as Hotel_Owner;
};

export const partialUpdateHotelOwner = async (hotelOwnerId: number, partialData: Partial<Hotel_Owner>) => {
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
    const url = `${API_BASE_URL}/hotel-owners/${hotelOwnerId}/hotels/`;
    const response = await axios.delete(url);
    return response.data;
};
