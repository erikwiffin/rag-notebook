import { useQuery } from "@apollo/client";
import { gql } from "../__generated__/gql";
import { Document } from "../__generated__/graphql";
import { ChangeEventHandler, useState } from "react";

const SEARCH = gql(`
  query SEARCH($text: String!) {
    search(text: $text) {
      id
      text
    }
  }
  `);

const SearchInput = ({ text, setText }: { text: string; setText: any }) => {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setText(event.target.value);
  };

  return (
    <div>
      <label className="input input-bordered flex items-center gap-2">
        <input
          type="text"
          className="grow"
          placeholder="Search"
          value={text}
          onChange={handleChange}
        />
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          className="h-4 w-4 opacity-70"
        >
          <path
            fillRule="evenodd"
            d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
            clipRule="evenodd"
          />
        </svg>
      </label>
    </div>
  );
};

const SearchResults = ({
  loading,
  error,
  results,
}: {
  loading: boolean;
  error: any;
  results: Document[] | undefined;
}) => {
  if (loading) {
    return <span className="loading loading-spinner loading-md"></span>;
  }
  if (error) {
    return <>{`${error}`}</>;
  }

  return (
    <div>
      {results?.map((result) => (
        <SearchResult key={result.id} result={result} />
      ))}
    </div>
  );
};

const SearchResult = ({ result }: { result: Document }) => (
  <div>
    <h4>ID: {result.id}</h4>
    <div className="truncate">{result.text}</div>
  </div>
);

export const Search = () => {
  const [text, setText] = useState("");
  const { loading, error, data } = useQuery(SEARCH, {
    variables: { text },
  });

  return (
    <div>
      <SearchInput text={text} setText={setText} />
      <SearchResults loading={loading} error={error} results={data?.search} />
    </div>
  );
};
