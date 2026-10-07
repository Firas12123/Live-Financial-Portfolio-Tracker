import React from 'react';
import {Currencies} from '../constants/currencies.js';
import '../App.css'

const currency = Object.entries(Currencies)
export const Currency_buttons = ({curClass, currentPick}) => {
    return (
        <div className={curClass}>
            {currency.map(([name, symbol]) => {
                return(
            <button key={name} className="currency-button" onClick={() => currentPick(name, symbol)}>
                {name} {symbol}
            </button>
                )
            })}
        </div>
    )}
