import React from 'react';
import '../styles/InfoPaneStyles.css';

const InfoPane = (props) => {
    return (
        <div className='info-pane'>
            <div className="city-name-info">
                <h1>{props.city}</h1>
                <h2>
                    ({props.lat}, {props.lon})
                </h2>
            </div>
            <div className="extra-details">
                {props.temp}
                <br></br>
                Rendered Area: 21.8 sq. mi
                <br></br>
                Mesh Cells used: 24 (6x4)
                <br></br>
                Maximum Temperature: 27 C
                <br></br>
                Minimum Temperature: 18 C

            </div>
            <TimeControls selectTime={props.selectTime} active={props.currDay}/>
        </div>
    );
};

const TimeControls = (props) => {
    return (
        <div className='time-controls-container'>

            {[0, 1, 2, 3, 4, 5, 6].map((day) => {
                return (
                    <button
                    onClick={() => {props.selectTime(day)}}
                    className={`time-control-button${day === props.active? ' active':''}`}>Jun {20 + day}
                    </button>
                );
            })}
        </div>
    );
};

export default InfoPane;