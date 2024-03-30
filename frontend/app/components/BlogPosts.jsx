import React,{useEffect, useRef} from "react";

const Blog = () => {

    const videoRef = useRef(null);

    useEffect(() => {
        const video = videoRef.current;

        const handleScroll = () => {
            const rect = video.getBoundingClientRect();
            const windowHeight = window.innerHeight || document.documentElement.clientHeight;

            // Check if the video is in view
            if (rect.top >= 0 && rect.bottom <= windowHeight) {
                video.play();
            } else {
                video.pause();
            }
        };

        window.addEventListener('scroll', handleScroll);

        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    return (
        <section className="mt-12 mx-auto px-4 max-w-screen-xl md:px-8">
            <div className="text-center">
                <h1 className="text-3xl text-yellow-400 font-semibold">
                    See the Demo Instruction Video Here
                </h1>
                <p className="mt-3 text-white">
                    Please Follow this Video Carefully, to take your Dose.
                </p>
            </div>
            <div className="">
                <video ref={videoRef} loop muted playsInline className="w-full h-auto">
                    <source src="/Demo1.mp4" type="video/mp4"/>
                    Your browser does not support the video tag.
                </video>
            </div>
        </section>
    );
}

export default Blog;
