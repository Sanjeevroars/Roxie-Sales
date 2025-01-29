import { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlay, faArrowLeft, faArrowRight } from "@fortawesome/free-solid-svg-icons";

const images = [
  "/homepage/hero01.jpg",
  "/homepage/hero02.jpg",
  "/homepage/hero03.jpg"
];

const Slider = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  // Function to move to the next slide
  const nextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
  };

  // Function to move to the previous slide
  const prevSlide = () => {
    setCurrentIndex((prevIndex) =>
      prevIndex === 0 ? images.length - 1 : prevIndex - 1
    );
  };

  // Automatically move to the next slide every 1 second
  useEffect(() => {
    const interval = setInterval(nextSlide, 2000);

    // Cleanup the interval on component unmount
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex justify-center">
      {/* Centered div with background image */}
      <div
        className="relative w-[100vw] h-[70vh] bg-cover bg-center"
        style={{
          backgroundImage: `url(${images[currentIndex]})`,
        }}
      >
        {/* Learn More Button */}
        <div className="absolute bottom-8 left-8 z-10">
          <button className="px-6 py-3 bg-white text-black font-semibold">
            Learn More
          </button>
        </div>

        {/* Slider Navigation Buttons */}
        <div className="absolute bottom-8 right-8 flex items-center gap-3 z-10">
          {/* Previous Arrow Button */}
          <button
            onClick={prevSlide}
            className="w-12 h-12 bg-transparent flex justify-center items-center border-2 border-black border-white hover:bg-blue-500 hover:border-blue-500 hover:text-white transition-all duration-200"
          >
            <FontAwesomeIcon icon={faArrowLeft} />
          </button>

          {/* Current Slide Indicator */}
          <button
            onClick={nextSlide}
            className="w-12 h-12 bg-transparent flex justify-center items-center border-2 border-black hover:bg-blue-500 hover:border-blue-500 hover:text-white transition-all duration-200"
          >
            <span className="text-xl">{`${currentIndex + 1}/3`}</span>
          </button>

          {/* Next Arrow Button */}
          <button
            onClick={nextSlide}
            className="w-12 h-12 bg-transparent flex justify-center items-center border-2 border-black hover:bg-blue-500 hover:border-blue-500 hover:text-white transition-all duration-200"
          >
            <FontAwesomeIcon icon={faArrowRight} />
          </button>

          {/* Play Button */}
          <button className="w-20 h-12 bg-black text-white flex justify-center items-center shadow-md ml-5 hover:bg-gray-700 transition-all duration-200">
            <FontAwesomeIcon icon={faPlay} className="mr-2" />
            Play
          </button>
        </div>
      </div>
    </div>
  );
};

export default Slider;
