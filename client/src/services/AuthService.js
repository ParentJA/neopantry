export const getUser = () => {
  return JSON.parse(window.localStorage.getItem('neopantry.user'));
};
