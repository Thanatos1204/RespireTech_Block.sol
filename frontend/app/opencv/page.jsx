'use client'
import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import Nav from '../components/Navbar';
import RectangleScreen from '../components/RectangleScreen';
import { UserAuth } from "../context/AuthContext";
import ShakesChart from "../components/ui/ShakesChart";
import PumpsChart from "../components/ui/PumpsChart";

const OpenCV = () => {

    const { user, logOut } = UserAuth();
    const [email, setEmail] = useState();
    // useEffect(() => {
    //     if(user){
    //         console.log(user.email);
    //         setEmail(user.email); 
    //     }else{
    //         console.log("Email Not Found");
    //     }
    // }, [user]);

    const shakesData = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [
          {
            label: 'Shakes per Second',
            data: [10, 20, 15, 25, 30, 20, 35],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
          },
        ],
      };// Example data for shakes per second
      const pumpsData = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [
          {
            label: 'Pumps per Day',
            data: [2, 4, 3, 5, 6, 4, 7],
            borderColor: 'rgb(255, 99, 132)',
            tension: 0.1,
          },
        ],
      };
       // Example data for pumps per day

  return (
        <Layout>
            <Nav/>
            <RectangleScreen>
                <section className='flex flex-col items-center justify-center gap-4'>
                    <div className='flex justify-evenly gap-8'>
                        <h1 className=' text-5xl'> Hello <span className='text-yellow-400'>{email}</span></h1>
                        <a href='/'> <button className='text-2xl' onClick={async () => { await logOut() }}>Log Out</button></a>
                    </div>
                    <div className='flex justify-center items-center gap-3'>
                        <div className="text-center">                    
                            <img className=' items-center' src="http://localhost:5000/video_feed" autoplay></img>
                        </div>

                        <div className="flex  flex-col justify-center gap-8">
                            <div className="chart-container">
                                <ShakesChart data={shakesData}/>
                            </div>
                            <div className="chart-containe">
                                <PumpsChart data={pumpsData}/>
                            </div>
                        </div>
                    </div>
                    
                </section>
            </RectangleScreen>
        </Layout>    
  )
}        

export default OpenCV;
