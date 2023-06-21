import './App.css';
import Selector from './components/Selector';
import Frame from './components/Frame'
import { useState } from 'react';

const location_data = require('./data/city_locations.json')
const id_map = require('./data/city_ids.json')

function App() {

  function onSelectCity(city) {
    console.log(city + " id was selected");
    setCity(city);

    const lat = location_data[city].latitude;
    const lon = location_data[city].longitude;

    fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=64515aae99f7cae97f61cbf76226826b`)
    .then(response => response.json())
    .then(data => {
      setCurrCityData(data);
    })
    .catch(error => {});

    // Set color data and temp data
  }

  function selectTime(day) {
    setCurrDisplayDay(day);
  }

  const [currDisplayDay, setCurrDisplayDay] = useState(0);

  const [city, setCity] = useState(0);
  const [currCityData, setCurrCityData] = useState({
    main: {
      temp: 0
    }
  });

  // get these from the API
  const [currColorData, setCurrColorData] = useState(
    [
      [[255,0,0],[255,120,0],[255,137,0],[255,189,56],[215,120,0],[230,250,40]],
      [[240,220,0],[185,190,0],[255,80,0],[200,160,50],[170,130,10],[90,180,20]],
      [[255,170,0],[60,180,160],[255,120,0],[255,90,0],[230,120,0],[30,140,110]],
      [[25,170,70],[20,170,100],[120,190,10],[25,170,255],[50,90,200],[25,100,190]]
    ]
  );
  const [currTempData, setCurrTempData] = useState(
    [
      ["-1 C","-2 C","-3 C","-4 C","-5 C","-6 C"],
      ["-7 C","-8 C","-9 C","-10 C","-11 C","-12 C"],
      ["-13 C","-14 C","-15 C","-16 C","-17 C","-18 C"],
      ["-19 C","-20 C","-21 C","-22 C","-23 C","-24 C"]
    ]
  );

  let temp;
  try {
    temp = `Current Temperature: ${Math.round(currCityData.main.temp - 273.15)} C`;
  } catch (error) {}



  return (
    <div className="main-section">
      <Selector selectCity={onSelectCity}/>
      <Frame
        city={id_map[city]} 
        lat={location_data[city].latitude} 
        lon={location_data[city].longitude} 
        temp={temp}
        selectTime={selectTime}
        currDisplayDay={currDisplayDay}
        colorData={currColorData}
        tempData={currTempData}
        cityImgFile={id_map[city].split(' ').join('_') + '.png'}
        />
    </div>
  );
}

export default App;
