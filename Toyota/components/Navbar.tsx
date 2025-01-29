"use client";

import Link from "next/link";

const NavBar = () => {
  const handleRedirect = () => {
    window.location.href = "http://localhost:3009";
  };

  return (
    <header className="w-full absolute z-10">
      <nav className="max-w-[1440px] mx-auto flex justify-between items-center sm:px-16 px-6 py-4 bg-transparent">
        <Link href="/" className="flex justify-center items-center">
          {/* Your logo here, you can uncomment if needed */}
          {/* <Image
            src='/logo.svg'
            alt='logo'
            width={118}
            height={18}
            className='object-contain'
          /> */}
        </Link>

        {/* Dashboard Button */}
        <button
          title="Dashboard"
          type="button"
          className="text-[#2751E9] rounded-full bg-white min-w-[130px] py-2 px-4 text-center"
          onClick={handleRedirect}
        >
          Dashboard
        </button>
      </nav>
    </header>
  );
};

export default NavBar;
