import { useContext } from "react";
import { AppContext } from "./context/AppContext";

export const App = () => {
  const {} = useContext(AppContext);
  return (
    <>
      <h1>RAG Playground</h1>
    </>
  );
};
