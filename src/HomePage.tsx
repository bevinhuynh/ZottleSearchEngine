import {applyHomePageTheme,  changeThemeMode, fetch_query_results, handleLuckyButton} from "./helpers"
import './App.css'
import AboutHeader from "./AboutHeader"
import { useNavigate } from "react-router";
import { useEffect } from "react";

function HomePage() {
  useEffect(() => {
    applyHomePageTheme();
  }, [])
  const navigate = useNavigate();
  
  const handleClick = async () => {
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

  const handleLuckyClick = async () => {
    const results = await handleLuckyButton();
    navigate("/search", { 
      state: {
        searchResults: results,
        query: results[2]
      }
    })
  }

  // const navigateToAbout = () => {
  //   navigate("/about");
  // }

  return (
    <>
      
      <AboutHeader/>
      <div className='container-fluid' id="main-container">
        <div className='row'>
          <a>
            <img src="../src/assets/anteater.svg" className="anteater" alt="Anteater logo" id="anteater" />
          </a>
        </div>
        <div className='row' id='title'>
          <h1 id='zottle-logo'><span className="letter z">Z</span>
          <span className="letter o1">o</span>
          <span className="letter t1">t</span>
          <span className="letter t2">t</span>
          <span className="letter l">l</span>
          <span className="letter e">e</span></h1>
        </div>
        <div className='row' id='searchbar'>
          <form id='search-bar-form'>
            <input id='search-bar' placeholder='Search Zoogle'></input>
            <a onClick={handleClick}>
              <img id='search-img' src='../src/assets/searchimg.svg'></img>
            </a>
          </form>
        </div>
        <div className='row' id="buttons">
          <div className='col' id='search-button'>
            <button onClick={handleClick}>Zoogle Search</button>
          </div>
          <div className='col' id='lucky-button'>
            <button onClick={handleLuckyClick}>I'm feeling lucky</button> 
          </div>
        </div>      
      </div>
      <footer className="mt-auto " id='setting-footer'>
          <div>
            <p id='footer-content' onClick={changeThemeMode}>Dark Mode</p>
          </div>
        </footer>
    </>
  )
}

export default HomePage