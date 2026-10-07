import {PieChart} from './components/Pie.jsx';
import {useState, useEffect} from 'react'
import './App.css';
import {Currency_buttons} from './components/currencies.jsx';

function App() {
        const [portfolioData, SetPortfolioData] = useState(null)
        const [currency, currencySet] = useState(() => {
            const saved = localStorage.getItem("currency")
            return saved ? saved : "GBP";
        });
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
            if (data.status === 200) {
                SetPortfolioData(data.data)
            }
        }
        useEffect(() => {
            localStorage.setItem("currency", currency)
            sendPortfolioData(currency);
        }, [currency])
    function saveCurrency(name, symbol){
        localStorage.setItem("currency", name)
        localStorage.setItem("symbol", symbol)
        currencySet(name)
        setCurrencies(false)
    }
    const currency_cur = localStorage.getItem("currency") || "GBP"
    const currency_symb = localStorage.getItem("symbol") || "£"
    const [currencies, setCurrencies] = useState(false);

    return (
        <>
    <nav id="top-nav">
        <div id="cur-div">
            <button className="main-font currency-button" id="current-currency" onClick={() => setCurrencies(!currencies)}>{currency_cur} {currency_symb}</button>
            <Currency_buttons curClass={currencies ? "currencies active" : "currencies"} currentPick={saveCurrency}/>
        </div>
    </nav>
    <div className="pie-chart">
        <PieChart id="pie" symbol = {currency_symb} portfolio={portfolioData}/>
    </div>
        </>
    );
}
export default App;

