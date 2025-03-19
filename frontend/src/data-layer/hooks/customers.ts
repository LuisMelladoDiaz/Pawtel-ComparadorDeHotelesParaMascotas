import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { type MaybeRef, toValue } from 'vue';
import {
    fetchAllOwners,
    fetchCustomerById,
    createCustomer,
    updateCustomer,
    partialUpdateCustomer,
    deleteCustomer,
    getCurrentCustomer,
    type Customer,
    fetchMyBookings,
} from '@/data-layer/api/customers';


export const useGetAllCustomers = () => {
    return useQuery({
        queryKey: ['customers'],
        queryFn: fetchAllOwners,
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });
};

export const useGetCustomerById = (customerId: MaybeRef<number>) => {
    return useQuery({
        queryKey: ['customerId', customerId],
        queryFn: () => fetchCustomerById(toValue(customerId)),
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });
};

export const useCreateCustomer = () => {
    return useMutation({
        mutationFn: createCustomer,
    });
};

export const useUpdateCustomer = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ customerId, ownerData }: { customerId: number; ownerData: Customer }) =>
            updateCustomer(customerId, ownerData),
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ['customer', data.id] });
        },
    });
};

export const usePartialUpdateCustomer = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ customerId, partialData }: { customerId: number; partialData: Partial<Customer> }) =>
            partialUpdateCustomer(customerId, partialData),
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ['customer', data.id] });
        },
    });
};

export const useDeleteCustomer = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: deleteCustomer,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['customers'] });
        },
    });
};


export const useGetCurrentCustomer = () => {
    return useQuery({
        queryKey: ['currentCustomer'],
        queryFn: () => getCurrentCustomer(),
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });
}

export const useGetMyBookings = () => {
    return useQuery({
      queryKey: ['my-bookings'],
      queryFn: fetchMyBookings,
      staleTime: 1000 * 60,
      refetchOnWindowFocus: false,
    });
  };
  