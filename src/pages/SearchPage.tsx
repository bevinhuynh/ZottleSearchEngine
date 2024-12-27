import { useLocation } from "react-router";
import SearchHeader from "../components/SearchHeader";
import QueryDisplay from "../components/QueryDisplay";
import { applyTfidfColor, changeSearchPageTheme } from "../helpers";
import { useEffect } from "react";

function SearchPage() {
  useEffect(() =>{
    applyTfidfColor();
  }, []);
  const results = useLocation();  // Extract search results from useLocation
  // console.log(results.state)
  const urlArray = results.state.searchResults[0]
  const queryTime = results.state.searchResults[1].toFixed(2);


  
  return (
    <>
    <div id="searchpage-container">
      <div className="container" id="header-container">
          <div className="row">
            <SearchHeader queryValue={results.state.query}/>
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
        <footer id='setting-footer-searchpage'>
            <p id='footer-content-searchpage' onClick={changeSearchPageTheme}>Dark Mode</p>
            <p id='query-time'>Search result processed in {queryTime} milliseconds</p>
            {/* <a href='https://www.google.com/'id='about-in-footer'>About</a>   */}
            {/* <p id='about-in-footer' onClick>About</p> */}
            <a href='https://github.com/TaylorTraan/SearchEngine' id='github-in-footer'>Github</a>                                  

        </footer>     
    </div>
    </>
  );
}

export default SearchPage;
