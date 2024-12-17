import { useLocation } from "react-router";
import SearchHeader from "../components/SearchHeader";
import QueryDisplay from "../components/QueryDisplay";

function SearchPage() {
  const results = useLocation();  // Extract search results from useLocation
  const urlArray = results.state.searchResults[0]
  
  return (
    <>
     <SearchHeader/>
    </>
  );
}

export default SearchPage;
 {/* <div className="container">
        {urlArray.length > 0 ? (
          urlArray.map((result: any, index: number) => (
            <QueryDisplay key={index} url={result[0]} tfidf={result[1]} />
          ))
        ) : (
          <h1>No results found.</h1>
        )}
      </div> */}