import React from 'react';
import '../styles/SelectorStyles.css';

const Selector = (props) => {
    return (
        <div className="selector">
            Select City:
            <select className='city-select' onChange={(choice) => props.selectCity(choice.target.value)}>
            <option className='city-option' value="1">New York</option>
            <option className='city-option' value="2">Los Angeles</option>
            <option className='city-option' value="3">Chicago</option>
            </select>
        </div>
    );
};

export default Selector;