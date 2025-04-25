import api from "@/api";

export type HotelImage = {
  id?: number;
  image: File;
  is_cover: boolean;
  hotel_id: number;
};

export const fetchHotelImage = async (hotelId: number, imageId: number) => {
  const url = `hotels/${hotelId}/hotel-images/${imageId}/`;
  const response = await api.get(url);
  return await response.json<HotelImage>();
};

export const fetchAllHotelImages = async (hotelId: number) => {
  const url = `hotels/${hotelId}/hotel-images/all/`;
  const response = await api.get(url);
  return await response.json<HotelImage[]>();
};

export const uploadHotelImage = async (hotelId: number, image: File, isCover: boolean) => {
  const formData = new FormData();
  formData.append("image", image, image.name);
  formData.append("is_cover", isCover ? "true" : "false");

  const url = `hotels/${hotelId}/hotel-images/upload/`;
  const response = await api.post(url, { body: formData });
  return await response.json<HotelImage>();
};

export const updateHotelImage = async (hotelId: number, imageId: number, image: string, isCover: boolean) => {
  const url = `hotels/${hotelId}/hotel-images/${imageId}/update/`;
  const response = await api.put(url, { json: { image, is_cover: isCover } });
  return await response.json<HotelImage>();
};

export const partialUpdateHotelImage = async (hotelId: number, imageId: number, image: string, isCover: boolean) => {
  const url = `hotels/${hotelId}/hotel-images/${imageId}/patch/`;
  const response = await api.patch(url, { json: { image, is_cover: isCover } });
  return await response.json<HotelImage>();
};

export const deleteHotelImage = async (hotelId: number, imageId: number) => {
  const url = `hotels/${hotelId}/hotel-images/${imageId}/delete/`;
  const response = await api.delete(url);
  return await response.json();
};

export const setCoverImage = async (hotelId: number, imageId: number) => {
  const url = `hotels/${hotelId}/hotel-images/${imageId}/set-is-cover/`;
  const response = await api.put(url, { json: { is_cover: true } });
  return await response.json<HotelImage>();
};

export const unsetCoverImage = async (hotelId: number, imageId: number) => {
  const url = `hotels/${hotelId}/hotel-images/${imageId}/set-is-cover/`;
  const response = await api.put(url, { json: { is_cover: false } });
  return await response.json<HotelImage>();
};

export const fetchCoverImage = async (hotelId: number) => {
  const url = `hotels/${hotelId}/hotel-images/cover/`;
  const response = await api.get(url);
  return await response.json<HotelImage>();
};

export const fetchNonCoverImages = async (hotelId: number) => {
  const url = `hotels/${hotelId}/hotel-images/non-cover/`;
  const response = await api.get(url);
  return await response.json<HotelImage[]>();
};
