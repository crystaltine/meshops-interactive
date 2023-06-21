import React from 'react';
import '../styles/HeatmapOverlayStyles.css';
import '../styles/OverlayPopup.css';

const HeatmapOverlay = (props) => {
    /*
    Requires data (array of [r,g,b] representing color codes for relative heat at each point)
    */
    return (
        <div class="heatmap">
            {props.data.map((row, rowIndex) => {
                return (
                    props.tempData === undefined?
                    <></> :
                    <HeatmapRow data={row} rowIndex={rowIndex} tempData={props.tempData}/>
                );
            })}
        </div>
    );
};

const HeatmapRow = (props) => {
    return (
        <div class="heatmap-row">
            {props.data.map((color, colIndex) => {
                return (
                    <div 
                    className="heatmap-cell parent" 
                    style={{
                        backgroundColor: `rgb(${color[0]},${color[1]},${color[2]},0.2)`
                    }}>

                        <div className="popup">
                            {props.tempData[props.rowIndex][colIndex]}
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default HeatmapOverlay;