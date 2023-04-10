import React, { createContext, useState } from "react";

export const UserContext = createContext({});

export const UserProvider = (props) => {
  const [tokenInfo, setUserState] = useState(
    JSON.parse(localStorage.getItem("user_info"))
  );

  console.log(tokenInfo);

  return (
    <UserContext.Provider value={tokenInfo}>
      {props.children}
    </UserContext.Provider>
  );
};
