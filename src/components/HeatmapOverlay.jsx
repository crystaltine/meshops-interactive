import React from 'react';
import '../styles/HeatmapOverlayStyles.css';
import '../styles/OverlayPopup.css';

const HeatmapOverlay = (props) => {
    console.log('recieved basline temp: ' + props.baselineTemp + ' and interval width: ' + props.intervalWidth);
    /*
    Requires data (array of [r,g,b] representing color codes for relative heat at each point)
    */
    return (
        <div class="heatmap">
            {props.data.map((row, rowIndex) => {
                return (
                    props.tempData === undefined?
                    <></> :
                    <HeatmapRow 
                        data={row} 
                        rowIndex={rowIndex} 
                        tempData={props.tempData}
                        baseLine={props.baselineTemp}
                        intervalWidth={props.intervalWidth}
                    />
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
                            {`${Math.round((Number(props.baseLine) + Number(props.intervalWidth)*props.tempData[props.rowIndex][colIndex]) * 100) / 100}C (${Math.round(100*(Math.round((Number(props.baseLine) + Number(props.intervalWidth)*props.tempData[props.rowIndex][colIndex]) * 100) / 100) * 9/5 + 32)/100}F)`}
                        </div>
                    </div>
                );
            })}
        </div>
    );
};

export default HeatmapOverlay;