import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { fetchBookingHoldById, fetchAllBookingHolds, createBookingHold, deleteBookingHold } from '@/data-layer/api/bookingholds';

export const useGetBookingHoldById = (id: number) => {
    return useQuery({
        queryKey: ['booking-hold', id],
        queryFn: () => fetchBookingHoldById(id),
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
        enabled: !!id,
    });
};

export const useGetAllBookingHolds = () => {
    return useQuery({
        queryKey: ['booking-holds'],
        queryFn: fetchAllBookingHolds,
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });
};

export const useCreateBookingHold = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: createBookingHold,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['booking-holds'] });
        },
    });
};

export const useDeleteBookingHold = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: deleteBookingHold,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['booking-holds'] });
        },
    });
};
