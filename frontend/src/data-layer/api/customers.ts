import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export type Customer = {
    id?: number;
    username: string;
    email: string;
    phone: string;
    password: string;
    date_joined?: string;
    last_login?: string;
    is_active?: boolean;
};


export const fetchAllOwners = async () => {
    const url = `${API_BASE_URL}/api/customers/`;
    const response = await axios.get(url);
    return response.data as Customer[];
};

export const fetchCustomerById = async (CustomerId: number) => {
    const url = `${API_BASE_URL}/customers/${CustomerId}`;
    const response = await axios.get(url);
    return response.data as Customer;
};

export const createCustomer = async (CustomerData: Omit<Customer, 'id'>) => {
    const url = `${API_BASE_URL}/auth/register/`;
    try {
        const response = await axios.post(url, {...CustomerData, role: "customer"});
        return response.data as Customer;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error("Error en la solicitud:", error.response?.data);
            throw new Error(error.response?.data?.detail || 'Error desconocido');
        } else {
            console.error("Error desconocido:", error);
            throw new Error('Error desconocido');
        }
    }
};

export const updateCustomer = async (CustomerId: number, ownerData: Customer) => {
    const url = `${API_BASE_URL}/customers/${CustomerId}/`;
    const response = await axios.put(url, ownerData);
    return response.data as Customer;
};

export const partialUpdateCustomer = async (CustomerId: number, partialData: Partial<Customer>) => {
    const url = `${API_BASE_URL}/customers/${CustomerId}/`;
    const response = await axios.patch(url, partialData);
    return response.data;
};

export const deleteCustomer = async (CustomerId: number) => {
    const url = `${API_BASE_URL}/customers/${CustomerId}/`;
    const response = await axios.delete(url);
    return response.data;
};

export const getCurrentCustomer = async () => {
    const url = `${API_BASE_URL}/customers/me`;
    const response = await axios.get(url);
    return response.data as Customer;
}
