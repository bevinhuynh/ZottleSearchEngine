// import "../App.css"
import { useNavigate } from "react-router-dom";
import "../css_files/SearchHeader.css"
import { fetch_query_results } from "../helpers";
import { useState } from "react";

interface SearchHeaderProps { 
    queryValue: string
}

const SearchHeader: React.FC<SearchHeaderProps> = ({queryValue}) => {
    const [searchInput, setSearchInput] = useState(queryValue);
    const navigate = useNavigate();
    const returnToHome = () => {
        navigate("/")
    };
    const searchQuery = async () => {
        const results = await fetch_query_results();
        if (results) {
            navigate("/search", { 
              state: {
                searchResults: results[0],
                query: results[1]
              }
            })
          }
        };
    return (
        <>
        <header id="search-header">
            <h1 id='zottle-logo-header' onClick={returnToHome}>
                <span className="letter z">Z</span>
                <span className="letter o1">o</span>
                <span className="letter t1">t</span>
                <span className="letter t2">t</span>
                <span className="letter l">l</span>
                <span className="letter e">e</span>
            </h1>
            <img src="../src/assets/anteater.svg" className="anteater" alt="Anteater logo" id="anteater-header"/>
            <form id='search-bar-form-header'>
                <input id='search-bar' placeholder='Search Zottle' value={searchInput} onChange={(e) => setSearchInput(e.target.value)}></input>
                <img id='search-img' src='../src/assets/searchimg.svg' onClick={searchQuery}></img>
            </form>
        </header>
        </>
    )
}

export default SearchHeader

                       
