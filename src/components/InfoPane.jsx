import React from 'react';
import '../styles/InfoPaneStyles.css';

const InfoPane = (props) => {

    console.log(props.tempRanges);
    const tempstrLOW = `Low: ${Math.round(Number(props.tempRanges[0]))}C (${Math.round(props.tempRanges[0] * 9/5 + 32)}F)`;
    const tempstrHIGH = `High: ${Math.round(Number(props.tempRanges[1]))}C (${Math.round(props.tempRanges[1] * 9/5 + 32)}F)`;

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
                Rendered Area: {props.renderedArea} sq. mi
                <br></br>
                Mesh Cells used: 864 (24x36)
                <br></br>
                {tempstrLOW}
                <br></br>
                {tempstrHIGH}
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
                    className={`time-control-button${day === props.active? ' active':''}`}>{9 + day}:00
                    </button>
                );
            })}
        </div>
    );
};

export default InfoPane;