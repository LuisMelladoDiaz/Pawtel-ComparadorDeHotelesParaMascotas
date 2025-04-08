import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { type MaybeRef, toValue } from 'vue';
import {
    fetchAllOwners,
    fetchHotelOwnerById,
    createHotelOwner,
    updateHotelOwner,
    partialUpdateHotelOwner,
    deleteHotelOwner,
    fetchAllHotelsOfOwner,
    deleteAllHotelsOfOwner,
    getCurrentHotelOwner,
    approveHotelOwner,
    type HotelOwner,
} from '@/data-layer/api/hotelOwners';


export const useGetAllHotelOwners = () => {
    return useQuery({
        queryKey: ['hotelOwners'],
        queryFn: fetchAllOwners,
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });
};

export const useGetHotelOwnerById = (hotelOwnerId: MaybeRef<number>) => {
    return useQuery({
        queryKey: ['hotelOwnerId', hotelOwnerId],
        queryFn: () => fetchHotelOwnerById(toValue(hotelOwnerId)),
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });
};

export const useCreateHotelOwner = () => {
    return useMutation({
        mutationFn: createHotelOwner,
    });
};

export const useUpdateHotelOwner = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ hotelOwnerId, ownerData }: { hotelOwnerId: number; ownerData: HotelOwner }) =>
            updateHotelOwner(hotelOwnerId, ownerData),
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ['hotelOwnerId', data.id] });
            queryClient.invalidateQueries({ queryKey: ['hotelsOfOwner', data.id] });
            queryClient.invalidateQueries({ queryKey: ['hotelId', data.id] });
        },
    });
};

export const usePartialUpdateHotelOwner = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ hotelOwnerId, partialData }: { hotelOwnerId: number; partialData: Partial<HotelOwner> }) =>
            partialUpdateHotelOwner(hotelOwnerId, partialData),
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ['hotelOwner', data.id] });
            queryClient.invalidateQueries({ queryKey: ['hotelsOfOwner', data.id] });
            queryClient.invalidateQueries({ queryKey: ['hotelId', data.id] });
        },
    });
};

export const useDeleteHotelOwner = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: deleteHotelOwner,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['hotelOwners'] });
        },
    });
};

export const useGetAllHotelsOfOwner = (hotelOwnerId: number, enabled: boolean) => {
    return useQuery({
        queryKey: ['hotelsOfOwner', hotelOwnerId, enabled],
        queryFn: () => fetchAllHotelsOfOwner(toValue(hotelOwnerId)),
        enabled: enabled,
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });
};

export const useDeleteAllHotelsOfOwner = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: deleteAllHotelsOfOwner,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['hotels'] });
            queryClient.invalidateQueries({ queryKey: ['hotelOwner'] });
        },
    });
};



export const useGetCurrentHotelOwner = () => {
    return useQuery({
        queryKey: ['currentHotelOwner'],
        queryFn: () => getCurrentHotelOwner(),
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });
}

export const useApproveHotelOwner = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: approveHotelOwner,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['hotelOwners'] });
        },
    });
};
