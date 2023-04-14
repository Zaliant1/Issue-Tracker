import React, { createContext, useState } from "react";

export const UserContext = createContext({});

export const UserProvider = (props) => {
  const [tokenInfo, setUserState] = useState(
    JSON.parse(localStorage.getItem("user_info"))
  );

  const updateUserState = (newState) => {
    setUserState(newState);
    localStorage.setItem("userInfo", JSON.stringify(newState));
  };

  return (
    <UserContext.Provider value={{ tokenInfo, setUserState: updateUserState }}>
      {props.children}
    </UserContext.Provider>
  );
};
