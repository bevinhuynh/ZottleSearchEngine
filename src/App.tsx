// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
// import 'bootstrap/dist/css/bootstrap.min.css';


function App() {

  return (
    <>
      <div className='container-fluid'>
        <div className='row'>
          <a>
            <img src="../src/assets/anteater.svg" className="anteater" alt="Anteater logo" id="anteater" />
          </a>
        </div>
        <div className='row' id='title'>
          <h1>Zoogle</h1>
        </div>
        <div className='row' id='searchbar'>
          <form id='search-bar-form'>
            <input id='search-bar' placeholder='Search Zoogle'></input>
            <img id='searchimg' src='../src/assets/searchimg.svg'></img>
          </form>
        </div>
        <div className='row' id="buttons">
          <div className='col' id='search-button'>
            <button>Zoogle Search</button>
          </div>
          <div className='col' id='lucky-button'>
            <button>I'm feeling lucky</button> 
          </div>
        </div>
       
      </div>


      {/* <h1>Zoogle</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p> */}
    </>
  )
}

export default App
