import { PropsWithChildren, createContext } from "react";

type iAppContext = {};

const APP_CONTEXT_DEFAULTS: iAppContext = {} as const;

export const AppContext = createContext(APP_CONTEXT_DEFAULTS);

export const AppContextProvider = ({ children }: PropsWithChildren) => {
  return <AppContext.Provider value={{}}>{children}</AppContext.Provider>;
};
