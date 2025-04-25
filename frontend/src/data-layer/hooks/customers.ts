import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { type MaybeRef, toValue } from 'vue';
import {
    fetchAllOwners,
    fetchCustomerById,
    fetchCustomersByIds,
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

export const useGetCustomersByIds = (customerIds: MaybeRef<number[]>, opts) => {
    return useQuery({
        queryKey: ['customerIds', customerIds],
        queryFn: () => fetchCustomersByIds(toValue(customerIds)),
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
        enabled: opts?.enabled,
    });
}

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
            queryClient.invalidateQueries();
        },
    });
};

export const usePartialUpdateCustomer = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ customerId, partialData }: { customerId: number; partialData: Partial<Customer> }) =>
            partialUpdateCustomer(customerId, partialData),
        onSuccess: (data: any) => {
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
        queryKey: ['customer'],
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
