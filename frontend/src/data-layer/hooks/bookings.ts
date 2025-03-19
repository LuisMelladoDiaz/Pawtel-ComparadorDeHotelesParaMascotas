import { useQuery } from '@tanstack/vue-query';
import { type MaybeRef, toValue } from 'vue';
import { fetchAllBookings, fetchBookingById } from '../api/bookings';


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
