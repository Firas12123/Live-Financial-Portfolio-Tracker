import {PieChart} from './components/Pie.jsx';
import {useState, useEffect} from 'react'
import './App.css';


function App() {
        const [portfolioData, SetPortfolioData] = useState(null)
        const [currency, currencySet] = useState(() => {
            const saved = localStorage.getItem("currency")
            return saved ? saved : "GBP"
        } )
        const sendPortfolioData = async (selectedCurrency) => {
            const response = await fetch("http://127.0.0.1:5000/portfolio", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    currency: selectedCurrency
                })
            });
            const data = await response.json();
            if (data.status === 200){
                SetPortfolioData(data.data)
            }
        }
        useEffect(() => {
            localStorage.setItem("currency", currency)
            sendPortfolioData(currency);
        }, [currency])

    return (
        <>
    <nav id="top-nav">
        <button className="currency-button" onClick={() => currencySet('GBP')}>GBP</button>
    </nav>
    <div className="pie-chart">
        <PieChart portfolio={portfolioData}/>
    </div>
        </>
    );
}
export default App;

