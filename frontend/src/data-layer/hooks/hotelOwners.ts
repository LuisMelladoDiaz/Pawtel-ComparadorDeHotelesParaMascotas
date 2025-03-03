// src/hooks/useHotelOwners.ts
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
} from 'frontend/src/data-layer/api/hotelOwners.ts';

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
        onSuccess: (data) => {
            console.log('Dueño de hotel creado con éxito:', data);
        },
        onError: (error) => {
            console.error('Error al crear el dueño de hotel:', error);
        },
    });
};

export const useUpdateHotelOwner = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ hotelOwnerId, ownerData }: { hotelOwnerId: number; ownerData: Hotel_Owner }) =>
            updateHotelOwner(hotelOwnerId, ownerData),
        onSuccess: (data) => {
            console.log('Dueño de hotel actualizado:', data);
            queryClient.invalidateQueries({ queryKey: ['hotelOwner', data.id] });
        },
    });
};

export const usePartialUpdateHotelOwner = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ hotelOwnerId, partialData }: { hotelOwnerId: number; partialData: Partial<Hotel_Owner> }) =>
            partialUpdateHotelOwner(hotelOwnerId, partialData),
        onSuccess: (data) => {
            console.log('Dueño de hotel actualizado parcialmente:', data);
            queryClient.invalidateQueries({ queryKey: ['hotelOwner', data.id] });
        },
    });
};

export const useDeleteHotelOwner = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: deleteHotelOwner,
        onSuccess: () => {
            console.log('Dueño de hotel eliminado');
            queryClient.invalidateQueries({ queryKey: ['hotelOwners'] });
        },
    });
};

export const useGetAllHotelsOfOwner = (hotelOwnerId: number) => {
    return useQuery({
        queryKey: ['hotelsOfOwner', hotelOwnerId],
        queryFn: () => fetchAllHotelsOfOwner(hotelOwnerId),
        enabled: !!hotelOwnerId,
        staleTime: 1000 * 60,
        refetchOnWindowFocus: false,
    });
};

export const useDeleteAllHotelsOfOwner = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: deleteAllHotelsOfOwner,
        onSuccess: () => {
            console.log('Todos los hoteles del dueño eliminados');
            queryClient.invalidateQueries({ queryKey: ['hotels'] });
            queryClient.invalidateQueries({ queryKey: ['hotelOwner'] });
        },
    });
};
