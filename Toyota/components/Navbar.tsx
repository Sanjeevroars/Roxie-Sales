import Link from "next/link";
import Image from "next/image";

import CustomButton from "./CustomButton";

const NavBar = () => (
  <header className="w-full  absolute z-10">
    <nav className="max-w-[1440px] mx-auto flex justify-between items-center sm:px-16 px-6 py-4 bg-transparent">
      <Link href="/" className="flex justify-center items-center">
        {/* <Image
                    src='/logo.svg'
                    alt='logo'
                    width={118}
                    height={18}
                    className='object-contain'
                /> */}
      </Link>

      <button
        title="Welcome!"
        type="button"
        className="text-[#2751E9] rounded-full bg-white min-w-[130px] py-2 px-4 text-center"
      >
        Welcome!
      </button>
    </nav>
  </header>
);

export default NavBar;
