import React, {useState, useEffect} from "react";

function Timer(){
    const[seconds, setSeconds] = useState(0);
    
    useEffect(() => {
        const interval = setInterval(() => {
          setSeconds((seconds) => seconds + 1);
        }, 1000);
    
        return () => clearInterval(interval);
      }, []);   

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
    
    return(
        <p>Analysis In Progress - Time Elapsed: {hours}hrs {minutes}mins {remainingSeconds}s</p>
    )
}

export default Timer;