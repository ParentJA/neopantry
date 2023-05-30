import axios from 'axios';

export const getProfile = async () => {
  const url = '/api/v1/accounts/profile/';
  try {
    const response = await axios.get(url);
    return { response, isError: false };
  } catch (response) {
    return { response, isError: true };
  }
};

export const updateProfile = async (
  first_name,
  last_name,
  photo,
) => {
  const url = '/api/v1/accounts/profile/';
  const formData = new FormData();
  formData.append('first_name', first_name);
  formData.append('last_name', last_name);
  if (photo.length > 0) {
    formData.append('photo', photo);
  }
  try {
    const response = await axios.patch(url, formData);
    return { response, isError: false };
  } catch (response) {
    return { response, isError: true };
  }
};
