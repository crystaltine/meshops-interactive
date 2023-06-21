import React from 'react';
import '../styles/MapRendererStyles.css';
import HeatmapOverlay from './HeatmapOverlay';

const MapRenderer = (props) => {

    console.log(`url(${process.env.PUBLIC_URL}/city_maps/${props.cityImgFile})`);
    return (
        <div className="render-container">
            <div 
                className='map-renderer'
                style={{
                    backgroundImage: `url(${process.env.PUBLIC_URL}/city_maps/${props.cityImgFile})`,
                    backgroundSize: 'cover',
                }}>
                <HeatmapOverlay data={props.colorData} tempData={props.tempData}/>  
            </div> 
        </div>
    );
};

export default MapRenderer;