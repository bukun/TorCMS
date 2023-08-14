export const updateToken = (state, token) => {
  state.token = token;
  console.log('**************************')
  console.log(state)
};

export const updateUserInfo = (state, userInfo) => {
  state.userInfo = userInfo;
};

