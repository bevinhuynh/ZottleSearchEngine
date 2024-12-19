// import "../App.css"
import { useNavigate } from "react-router-dom";
import "../css_files/SearchHeader.css"

function SearchHeader() {
    const navigate = useNavigate();
    const returnToHome = () => {
        navigate('/')
    }
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
                <input id='search-bar-header' placeholder='Search Zottle'></input>
                <img id='search-img-header' src='../src/assets/searchimg.svg'></img>
            </form>
        </header>
        </>
    )
}

export default SearchHeader

                       
