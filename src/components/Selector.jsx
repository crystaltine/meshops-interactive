import React from 'react';
import '../styles/SelectorStyles.css';

const Selector = (props) => {
    return (
        <div className="selector">
            <div style={{borderRight:'2px solid white', paddingRight:'20px'}}>Meshops Interactive</div>
            Select City:
            <select className='city-select' onChange={(choice) => props.selectCity(choice.target.value)}>
            <option className='city-option' value="0">None</option>
            <option className='city-option' value="1">New York</option>
            <option className='city-option' value="2">Los Angeles</option>
            <option className='city-option' value="3">Chicago</option>
            </select>
            <div style={{marginLeft: "20px", fontSize:'17px', color:'#ffffff55'}}>*Temporarily using cached data, as API is unable to handle higher traffic.</div>
        </div>
    );
};

export default Selector;