import { useLocation } from "react-router";
import SearchHeader from "../components/SearchHeader";

function SearchPage() {
    const results = useLocation();
    console.log(results.state.searchResults)
    return (
       <>
        <SearchHeader/>
       </>
    )
}

export default SearchPage;