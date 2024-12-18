import { useLocation } from "react-router";
import SearchHeader from "../components/SearchHeader";
import QueryDisplay from "../components/QueryDisplay";

function SearchPage() {
  const results = useLocation();  // Extract search results from useLocation
  const urlArray = results.state.searchResults[0]
  console.log(urlArray)
  return (
    <>

     <div className="container" id="header-container">
      <div className="row">
        <SearchHeader/>
      </div>
     </div>
     <div id="total-container">
      <div className="container" id="url-container">
        {urlArray.length > 0 ? (
          urlArray.map((result: any, index: number) => (
            <div className="row" key={index} id="url-row"> 
                <QueryDisplay url={result[0]} tfidf={result[1].toFixed(2)} index_num={index+1} />
            </div>
          ))
        ) : (
          <h1>No results found.</h1>
        )}
      </div>
    </div>
    </>
  );
}

export default SearchPage;
