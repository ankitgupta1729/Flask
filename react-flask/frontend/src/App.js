import { useEffect,useState} from 'react';

function App() {
  const [data,setData] = useState({});
  useEffect(() => {
    fetchData();
  },[]);

  const fetchData = async () => {
    try{
      const response = await fetch('http://localhost:5000/api/data');
      const jsondata = await response.json();
      setData(jsondata);
    }
    catch(error){
      console.log("Error",error);
  }
  }
  return (
    <div className="App">
      <h1>React App</h1>
      <h3>{data.message}</h3>
    </div>
  );
}

export default App;
