import React from 'react';
import '../styles/MapRendererStyles.css';
import HeatmapOverlay from './HeatmapOverlay';

const MapRenderer = (props) => {

    if (props.cityImgFile === "Not_Selected.png") {
        return <div className='render-container'></div>
    }

    return (
        <div className="render-container">
            <div
                className='map-renderer'
                style={{
                    backgroundImage: `url(${process.env.PUBLIC_URL}/city_maps/${props.cityImgFile})`,
                    backgroundSize: 'cover',
                }}>
                <HeatmapOverlay 
                    data={props.colorData} 
                    tempData={props.tempData}
                    baselineTemp={props.currBaseline}
                    intervalWidth={props.intervalWidth}
                />
            </div>
        </div>
    );
};

export default MapRenderer;