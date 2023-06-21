import React from 'react';
import '../styles/FrameStyles.css';
import MapRenderer from './MapRenderer';
import InfoPane from './InfoPane';

const Frame = (props) => {
    console.log(`looking for image ${props.cityImgFile}`)
    return (
        <div className="main-frame">
            <MapRenderer 
                colorData={props.colorData} 
                tempData={props.tempData} 
                cityImgFile={props.cityImgFile}
            />
            <InfoPane
                city={props.city}
                temp={props.temp} 
                lat={props.lat} 
                lon={props.lon} 
                selectTime={props.selectTime} 
                currDay={props.currDisplayDay}
            />
        </div>
    );
};

export default Frame;