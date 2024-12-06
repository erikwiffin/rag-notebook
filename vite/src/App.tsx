import { useContext } from "react";
import { AppContext } from "./context/AppContext";
import { FileUpload } from "./components/FileUpload";
import { Search } from "./components/Search";

export const App = () => {
  const {} = useContext(AppContext);

  return (
    <>
      <div className="container mx-auto">
        <div className="columns-1 prose my-4">
          <h1>RAG Playground</h1>
        </div>
        <div className="w-full flex flex-row">
          <div className="w-1/3 flex-grow">
            <FileUpload />
          </div>
          <div className="w-1/2 flex-grow">
            <Search />
          </div>
        </div>
      </div>
    </>
  );
};
