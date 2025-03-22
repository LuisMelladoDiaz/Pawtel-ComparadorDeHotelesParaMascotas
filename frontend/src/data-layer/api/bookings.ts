import axios from 'axios';
import { useRouter } from 'vue-router';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const router = useRouter();

export type Booking = {
    id?: number;
    creation_date: string;
    start_date: string;
    end_date: string;
    total_price: number;
    customer: number;
    room_type: number;
};

export const createBooking = async (BookingData: Omit<Booking, 'id'>) => {
    const url = `${API_BASE_URL}/bookings/`;
    try {
        const response = await axios.post(url, {...BookingData, role: "customer"});

        if (response.data?.url) {
            window.location.href = response.data.url;  // Redirige al usuario a Stripe
            // router.go(response.data.url)
        }

        return response.data as string;
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
