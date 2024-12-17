// import "../App.css"
import "../css_files/SearchHeader.css"

function SearchHeader() {
    return (
        <>
        <header id="search-header">
            <h1 id='zottle-logo-header'>
                <span className="letter z">Z</span>
                <span className="letter o1">o</span>
                <span className="letter t1">t</span>
                <span className="letter t2">t</span>
                <span className="letter l">l</span>
                <span className="letter e">e</span>
            </h1>
            <img src="../src/assets/anteater.svg" className="anteater" alt="Anteater logo" id="anteater-header" />
            <form id='search-bar-form-header'>
                <input id='search-bar-header' placeholder='Search Zoogle'></input>
                <img id='search-img-header' src='../src/assets/searchimg.svg'></img>
            </form>
        </header>
        </>
    )
}

export default SearchHeader

                       
