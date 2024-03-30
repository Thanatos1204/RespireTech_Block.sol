'use client'
import React from 'react';
import Layout from '../components/Layout';
import Nav from '../components/Navbar';
import RectangleScreen from '../components/RectangleScreen';

const OpenCV = () => {
  return (
<Layout>
    <Nav/>
    <RectangleScreen>
        <section className='flex justify-center'>
                <div className="text-center">
                    
                    <img className=' items-center' src="http://localhost:5000/video_feed" autoplay></img>
                </div>
        </section>
    </RectangleScreen>
    
</Layout>
    
  )
}        

export default OpenCV;
