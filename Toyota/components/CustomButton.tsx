"use client";

import type { CustomButtonProps } from "../types";
import Image from "next/image";
import { FaPhone } from "react-icons/fa";
import axios from "axios"; // Import axios

const Button = ({
  isDisabled,
  btnType,
  containerStyles,
  textStyles,
  title,
  rightIcon,
  handleClick,
}: CustomButtonProps) => {
  const handleCallButtonClick = async () => {
    try {
      await axios.get("http://localhost:3001/run-exe");
      //   alert("The EXE was successfully executed!");
    } catch (error) {
      console.error("Error running the EXE:", error);
      alert("There was an error!");
    }
  };

  return (
    <button
      disabled={isDisabled}
      type={btnType || "button"}
      className={`custom-btn ${containerStyles}`}
      onClick={handleCallButtonClick}
    >
      <span className={`flex items-center ${textStyles}`}>
        Call Us Now
        <FaPhone className="ml-2 rotate-90" size={15} color="#ffffff" />
      </span>
      {rightIcon && (
        <div className="relative w-6 h-6">
          <Image
            src={rightIcon}
            alt="arrow_left"
            fill
            className="object-contain"
          />
        </div>
      )}
    </button>
  );
};

export default Button;
