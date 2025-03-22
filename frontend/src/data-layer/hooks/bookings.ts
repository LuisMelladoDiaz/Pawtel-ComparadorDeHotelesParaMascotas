import { useMutation } from '@tanstack/vue-query';
import { type Booking, createBooking } from '@/data-layer/api/bookings';

export const useCreateBooking = () => {
    return useMutation({
        mutationFn: createBooking,
    });
};
