import './App.css';
import Selector from './components/Selector';
import Frame from './components/Frame'
import { useState } from 'react';

const location_data = require('./data/city_locations.json')
const id_map = require('./data/city_ids.json')

function App() {

  /*
  function fetchFrames(cityName) {
    fetch(`127.0.0.1:5050/?city=${cityName}`)
    .then((response) => response.json())
    .then(data => {
      setFrames(data);
    })
  }
  */

  function onSelectCity(city) {
    console.log(city + " id was selected");

    if (city === '0') {
      console.log('city is 0')
      setCity(0);
      setCurrDisplayDay(0);
      setCurrCityData({
        main: {
          temp: 273.15
        }
      });
      setFrames({
        temps: Array(7).fill([[]]),
        colors: Array(7).fill([[[]]])
      });
      return;
    }

    const cachedColorFrames = require(`./data/display/colordata_${city}.json`);
    const cachedTempFrames = require(`./data/display/tempdata_${city}.json`);
    setFrames({
      temps: cachedTempFrames,
      colors: cachedColorFrames
    });
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
    //const temperatures = require(`./data/display/tempdata_${city}.json`);
    //const colors = require(`./data/display/colordata_${city}.json`);
    //setCurrTempData(temperatures);
    //setCurrColorData(colors);
  }

  function selectTime(day) {
    setCurrDisplayDay(day);
  }

  const [currDisplayDay, setCurrDisplayDay] = useState(0);
  const [city, setCity] = useState(0);
  const [currCityData, setCurrCityData] = useState({
    main: {
      temp: 273.15
    }
  });

  // get these from the API
  //const [currColorData, setCurrColorData] = useState([[[]]]);
  //const [currTempData, setCurrTempData] = useState([[]]);
  const [frames, setFrames] = useState({
    temps: Array(7).fill([[0]]),
    colors: Array(7).fill([[[0, 0, 0]]])
  });

  let temp = 'N/A';
  try {
    temp = (currCityData.main.temp - 273.15).toFixed(4);
  } catch (error) {}

  return (
    <div className="main-section">
      <Selector selectCity={onSelectCity}/>
      <Frame
        city={id_map[city]}
        cityId={city}
        lat={location_data[city].latitude} 
        lon={location_data[city].longitude} 
        temp={temp}
        selectTime={selectTime}
        currDisplayDay={currDisplayDay}
        cityImgFile={id_map[city].split(' ').join('_') + '.png'}
        areaRendered = {[0, 1200, 1250, 2400]}
        tempRanges = {[
          ["N/A", "N/A"],
          [-3, +2],
          [-2, +4],
          [-4, +3],
        ]}
        frames={frames}
        />
    </div>
  );
}

export default App;
