import { useMutation, useQuery } from '@tanstack/vue-query';
import { type Booking, createBooking } from '@/data-layer/api/bookings';
import { type MaybeRef, toValue } from 'vue';
import { fetchAllBookings, fetchBookingById } from '../api/bookings';


export const useCreateBooking = () => {
    return useMutation({
        mutationFn: createBooking,
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

export const useGetBookingById = (bookingId: MaybeRef<number>) => {
  return useQuery({
    queryKey: ['booking', bookingId],
    queryFn: () => fetchBookingById(toValue(bookingId)),
    staleTime: 1000 * 60,
    refetchOnWindowFocus: false,
  });
};
