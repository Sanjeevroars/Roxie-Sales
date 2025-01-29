import React from "react";

const TopSections = () => {
  const sections = [
    {
      title: "Laptops",
      image: "/top/top1.jpg", // Image 1
    },
    {
      title: "Desktops & all-in-ones",
      image: "/top/top2.jpg", // Image 2
    },
    {
      title: "Monitors",
      image: "/top/top3.jpg", // Image 3
    },
    {
      title: "PC Accessories",
      image: "/top/top4.jpg", // Image 4
    },
    {
      title: "AI Solutions",
      image: "/top/top5.jpg", // Image 5
    },
    {
      title: "Servers",
      image: "/top/top6.jpg", // Image 6
    },
    {
      title: "Data Storage",
      image: "/top/top7.jpg", // Image 7
    },
    {
      title: "Apex Multicloud & aaS",
      image: "/top/top8.jpg", // Image 8
    },
  ];

  return (
    <div className="m-20">
      <div className="grid grid-cols-4 gap-10 m-20">
        {sections.map((section, index) => (
          <div key={index} className="relative group">
            {/* Image */}
            <img
              src={section.image}
              alt={section.title}
              className="object-cover transition-all duration-300 group-hover:opacity-70" // Square size (w-32 h-32)
            />
            {/* Overlay and Title */}
            <div className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-40 group-hover:bg-opacity-60 transition-all">
              <div className="marg-left-neg absolute bg-black px-5 py-1 text-white font-semibold">
                {section.title}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TopSections;
