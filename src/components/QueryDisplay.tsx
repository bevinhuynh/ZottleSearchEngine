import "../App.css"

interface QueryDisplayProps {
    url: string;
    tfidf: number;
    index_num: number;
}

const QueryDisplay: React.FC<QueryDisplayProps> = ({url, tfidf, index_num}) =>  {
    return (
        <div>
            <a id="url-link" href={url}>{index_num}.&nbsp;&nbsp;{url}</a>
            <p className="tf-idf-score"> - TF-IDF score: {tfidf}</p>
        </div>
    )
    
}

export default QueryDisplay;