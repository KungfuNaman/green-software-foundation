import React, {useState, useEffect} from "react";

function Timer(){
    const[time, setTime] = useState(0);
    
    useEffect(() => {
        const interval = setInterval(() => {
          setTime((time) => time + 1);
        }, 1000);
    
        return () => clearInterval(interval);
      }, []);   
    
    return(
        <p>Loading - Time Elapsed: {time}s</p>
    )
}

export default Timer;