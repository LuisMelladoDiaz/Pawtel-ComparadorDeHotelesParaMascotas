import api from "@/api";

export type RoomType = {
  id?: number;
  name: string;
  description: string;
  capacity: number;
  num_rooms: number;
  price_per_night: number;
  pet_type: string;
  hotel: number;
  is_archived: boolean;
};

export const fetchRoomTypeById = async (roomTypeId: number) => {
  const url = `room-types/${roomTypeId}/`;
  const response = await api.get(url);
  return await response.json<RoomType>();
};

export const fetchRoomTypesByIds = async (roomTypeIds: number[]) => {
  const getUrl = (id: number) => `room-types/${id}/`;
  const requests = roomTypeIds.map((id) => api.get(getUrl(id)).json<RoomType>());
  const responses = await Promise.all(requests);
  return responses.reduce((acc, roomType) => {
    if (roomType.id !== undefined) {
      acc[roomType.id] = roomType;
    }
    return acc;
  }, {} as Record<number, RoomType>);
};

export const fetchAllRoomTypes = async (hotelId?: number) => {
  const url = hotelId ? `hotels/${hotelId}/room-types/` : `room-types/`;
  const response = await api.get(url);
  return await response.json<RoomType[]>();
};

export const createRoomType = async (roomTypeData: Omit<RoomType, "id">) => {
  const url = `room-types/`;
  const response = await api.post(url, { json: roomTypeData });
  return await response.json<RoomType>();
};

export const updateRoomType = async (roomTypeId: number, roomTypeData: Omit<RoomType, "id">) => {
  const url = `room-types/${roomTypeId}/`;
  const response = await api.put(url, { json: roomTypeData });
  return await response.json<RoomType>();
};

export const partialUpdateRoomType = async (roomTypeId: number, partialData: Partial<RoomType>) => {
  const url = `room-types/${roomTypeId}/`;
  const response = await api.patch(url, { json: partialData });
  return await response.json<RoomType>();
};

export const deleteRoomType = async (roomTypeId: number) => {
  const url = `room-types/${roomTypeId}/`;
  await api.delete(url);
};

export const checkRoomTypeAvailability = async (roomTypeId: number, startDate: string, endDate: string) => {
  const url = `room-types/${roomTypeId}/is-available?start_date=${startDate}&end_date=${endDate}`;
  const response = await api.get(url);
  return await response.json();
};

export const fetchHotelOfRoomType = async (roomTypeId: number) => {
  const url = `room-types/${roomTypeId}/hotel`;
  const response = await api.get(url);
  return await response.json();
};

export const fetchTotalVacancyForRoomType = async (roomTypeId: number) => {
  const url = `room-types/${roomTypeId}/total-vacancy/`;
  const response = await api.get(url);
  return await response.json<{ id: number; total_vacancy: number }>();
};

export const fetchVacancyForEachRoomInRoomType = async (roomTypeId: number) => {
  const url = `room-types/${roomTypeId}/rooms/vacancy/`;
  const response = await api.get(url);
  return await response.json<{ room_id: number; vacancy: number }[]>();
};
