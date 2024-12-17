import "../App.css"

interface QueryDisplayProps {
    url: string;
    tfidf: number;
}

const QueryDisplay: React.FC<QueryDisplayProps> = ({url, tfidf}) =>  {
    console.log(url)
    return (
        <div>
            <h1 id="url">{url}</h1>
        </div>
    )
    
}

export default QueryDisplay;


#search-header {
    /* background-color: black; */
    position: relative;
    margin-bottom: 43.5em;
    /* margin-right: 78em; */
    width: 90em;

}

#zottle-logo {
    font-family: sans-serif;
    letter-spacing: 1px;
    font-size: 2.3em;
    display: flex;
    margin-left: 1em;
    margin-top: 0.5em;
    width: fit-content;
  }

  .anteater {
    display: flex;
    height: 6.5em;
    will-change: filter;
    transition: filter 300ms;
    /* background-color: white; */
    margin-left: 10em;
    margin-top: -5em;
  }
  
.letter.z { color: #4285F4; }   /* Z (Blue) */
.letter.o1 { color: #EA4335; }  /* First o (Red) */
.letter.t1 { color: #FBBC05; }  /* Second o (Yellow) */
.letter.t2 { color: #4285F4; }   /* g (Blue) */
.letter.l { color: #34A853; }   /* l (Green) */
.letter.e { color: #EA4335; }   /* e (Red) */


#search-header {
    /* background-color: black; */
    position: relative;
    margin-bottom: 43.5em;
    /* margin-right: 78em; */
    width: 90em;

}