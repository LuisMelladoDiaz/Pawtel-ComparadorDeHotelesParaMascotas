import { useQuery } from '@tanstack/vue-query';
import { fetchBookingById, fetchAllBookings } from '@/data-layer/api/bookings';

export const useGetBookingById = (id: number) => {
    return useQuery({
        queryKey: ['booking', id],
        queryFn: () => fetchBookingById(id),
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
        enabled: !!id,
    });
};

export const useGetAllBookings = () => {
    return useQuery({
        queryKey: ['bookings'],
        queryFn: fetchAllBookings,
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });
};
