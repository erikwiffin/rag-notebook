import { useQuery } from "@apollo/client";
import { gql } from "../__generated__/gql";
import { Document } from "../__generated__/graphql";
import { useState } from "react";
import { debounce } from "lodash";

const SEARCH = gql(`
  query SEARCH($text: String!) {
    search(text: $text) {
      answer
      documents {
        id
        text
      }
    }
  }
  `);

const SearchInput = ({ text, setText }: { text: string; setText: any }) => {
  const [value, setValue] = useState(text);
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue(event.target.value);
    setText(event.target.value);
  };

  return (
    <div>
      <label className="input input-bordered flex items-center gap-2">
        <input
          type="text"
          className="grow"
          placeholder="Search"
          value={value}
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
  answer,
}: {
  loading: boolean;
  error: any;
  results: Document[] | undefined;
  answer: string | undefined;
}) => {
  if (loading) {
    return <span className="loading loading-spinner loading-md"></span>;
  }
  if (error) {
    return <>{`${error}`}</>;
  }

  return (
    <div>
      <div className="bg-base-300 rounded-lg p-4 my-4">{answer}</div>
      {results?.map((result) => (
        <SearchResult key={result.id} result={result} />
      ))}
    </div>
  );
};

const SearchResult = ({ result }: { result: Document }) => (
  <div className="border-b-base-300 border-b-2 p-2">
    <h4>ID: {result.id}</h4>
    <div className="">{result.text}</div>
  </div>
);

export const Search = () => {
  const [text, setText] = useState("What is Luna?");
  const { loading, error, data } = useQuery(SEARCH, {
    variables: { text },
  });

  return (
    <div>
      <SearchInput text={text} setText={debounce(setText, 1000)} />
      <SearchResults
        loading={loading}
        error={error}
        results={data?.search?.documents}
        answer={data?.search?.answer}
      />
    </div>
  );
};
