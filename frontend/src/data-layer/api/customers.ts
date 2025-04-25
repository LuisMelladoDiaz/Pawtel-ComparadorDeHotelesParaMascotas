import api from "@/api";

export type Customer = {
    id?: number;
    username: string;
    email: string;
    phone: string;
    password?: string;
    date_joined?: string;
    last_login?: string;
    is_active?: boolean;
    accept_terms?: boolean;
};

export type Booking = {
    id?: number;
    customer_id: number;
    room_type_id: number;
    start_date: string;
    end_date: string;
    total_price: number;
};

export const fetchAllOwners = async () => {
    const url = `customers/`;
    const response = await api.get(url);
    return await response.json<Customer[]>();
};

export const fetchCustomerById = async (CustomerId: number) => {
    const url = `customers/${CustomerId}`;
    const response = await api.get(url);
    return await response.json<Customer>();
};

export const fetchCustomersByIds = async (CustomerIds: number[]) => {
    const getUrl = (id: number) => `customers/${id}`;
    const requests = CustomerIds.map((id) => api.get(getUrl(id)).json<Customer>());
    const responses = await Promise.all(requests);
    return responses.reduce((acc, customer) => {
        if (customer.id !== undefined) {
            acc[customer.id.toString()] = customer;
        }
        return acc;
    }, {} as Record<string, Customer>);
};

export const createCustomer = async (CustomerData: Omit<Customer, "id">) => {
    const url = `auth/register/`;
    try {
        const response = await api.post(url, { json: { ...CustomerData, role: "customer" } });
        return await response.json<Customer>();
    } catch (error) {
        console.error(error);
        throw error;
    }
};

export const updateCustomer = async (CustomerId: number, ownerData: Customer) => {
    const url = `customers/${CustomerId}/`;
    const response = await api.patch(url, { json: ownerData });
    return await response.json<Customer>();
};

export const partialUpdateCustomer = async (CustomerId: number, partialData: Partial<Customer>) => {
    const url = `customers/${CustomerId}/`;
    const response = await api.patch(url, { json: partialData });
    return await response.json();
};

export const deleteCustomer = async (CustomerId: number) => {
    const url = `customers/${CustomerId}/`;
    const response = await api.delete(url);
    return await response.json();
};

export const getCurrentCustomer = async () => {
    const url = `customers/me`;
    const response = await api.get(url);
    return await response.json<Customer>();
};

export const fetchMyBookings = async () => {
    const url = `customers/my-bookings`;
    const response = await api.get(url);
    return await response.json<Booking[]>();
};
