import axios from 'axios';

export const getRecipe = async (id) => {
  const url = `/api/v1/recipes/${id}/`;
  try {
    const response = await axios.get(url);
    return { response, isError: false };
  } catch (response) {
    return { response, isError: true };
  }
};
