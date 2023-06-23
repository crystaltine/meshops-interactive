import React from 'react';
import '../styles/FrameStyles.css';
import MapRenderer from './MapRenderer';
import InfoPane from './InfoPane';

const Frame = (props) => {

    // NOTE: MapRenderer gets passed the color&temp data of the CURRENT DAY, App handles switching frames/days
      // Pass in the current frame to the Frame component based on the current day
    const currFrameTemps = props.frames.temps[props.currDisplayDay];
    const currFrameColors = props.frames.colors[props.currDisplayDay];

    const vartemp = Number(props.temp) + Number(props.currDisplayDay)/4;
    const tempRanges = [vartemp + props.tempRanges[props.cityId][0], vartemp + props.tempRanges[props.cityId][1]]
    const tempstr = `Temperature: ${Math.round(vartemp)}C (${Math.round(vartemp * 9/5 + 32)}F)`;

    return (
        <div className="main-frame">
            <MapRenderer 
                colorData={currFrameColors} 
                tempData={currFrameTemps} 
                cityImgFile={props.cityImgFile}
                currBaseline={Number(tempRanges[0])}
                intervalWidth={tempRanges[1] - tempRanges[0]}
            />
            <InfoPane
                city={props.city}
                tempRAW={vartemp}
                temp={tempstr} 
                lat={props.lat} 
                lon={props.lon} 
                selectTime={props.selectTime} 
                currDay={props.currDisplayDay}
                renderedArea={props.areaRendered[props.cityId]}
                tempRanges={tempRanges}
            />
        </div>
    );
};

export default Frame;