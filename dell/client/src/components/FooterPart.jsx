import React from "react";

const ListHeader = ({ children }) => {
  return <h3 className="font-semibold text-lg mb-2">{children}</h3>;
};

function FooterPart() {
  return (
    <footer>
      {/* Top Section */}
      <div className="bg-gray-100 text-sm text-gray-700 leading-6">
        <div className="max-w-screen-2xl mx-auto py-10 px-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <div className="relative inline-block">
                <button className="flex items-center bg-gray-100 text-sm font-medium border-none p-2">
                  🌐 IN/EN
                  <svg
                    className="w-4 h-4 ml-1"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M19 9l-7 7-7-7"
                    ></path>
                  </svg>
                </button>
                <div className="absolute hidden group-hover:block mt-2 bg-white shadow-lg rounded-md">
                  <ul>
                    <li className="px-4 py-2 hover:bg-gray-200">
                      India/English
                    </li>
                    <li className="px-4 py-2 hover:bg-gray-200">
                      Afghanistan/English
                    </li>
                    <li className="px-4 py-2 hover:bg-gray-200">
                      Australia/English
                    </li>
                    <li className="px-4 py-2 hover:bg-gray-200">
                      Bhutan/English
                    </li>
                    <li className="px-4 py-2 hover:bg-gray-200">
                      Maldives/English
                    </li>
                  </ul>
                </div>
              </div>
              <a href="#" className="block mt-4 text-gray-600 hover:underline">
                Site Map
              </a>
            </div>

            <div>
              <ListHeader>Account</ListHeader>
              <a href="#" className="block hover:underline">
                My Account
              </a>
              <a href="#" className="block hover:underline">
                Order Status
              </a>
              <a href="#" className="block hover:underline">
                My Products
              </a>
            </div>

            <div>
              <ListHeader>Support</ListHeader>
              <a href="#" className="block hover:underline">
                Support Home
              </a>
              <a href="#" className="block hover:underline">
                Contact Support
              </a>
            </div>

            <div>
              <ListHeader>Connect with Us</ListHeader>
              <a href="#" className="block hover:underline">
                Community
              </a>
              <a href="#" className="block hover:underline">
                Contact Us
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="bg-gray-100 text-sm text-gray-700 leading-6">
        <div className="max-w-screen-2xl mx-auto py-10 px-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <ListHeader>Our Offerings</ListHeader>
              <a href="#" className="block hover:underline">
                APEX
              </a>
              <a href="#" className="block hover:underline">
                Products
              </a>
              <a href="#" className="block hover:underline">
                Solutions
              </a>
              <a href="#" className="block hover:underline">
                Services
              </a>
            </div>

            <div>
              <ListHeader>Our Company</ListHeader>
              <a href="#" className="block hover:underline">
                Who We Are
              </a>
              <a href="#" className="block hover:underline">
                Careers
              </a>
              <a href="#" className="block hover:underline">
                Dell Technologies Capital
              </a>
              <a href="#" className="block hover:underline">
                Investors
              </a>
              <a href="#" className="block hover:underline">
                Newsroom
              </a>
              <a href="#" className="block hover:underline">
                Perspective
              </a>
              <a href="#" className="block hover:underline">
                Recycling
              </a>
              <a href="#" className="block hover:underline">
                ESG & Impact
              </a>
            </div>

            <div>
              <ListHeader>Our Partners</ListHeader>
              <a href="#" className="block hover:underline">
                Find a Partner
              </a>
              <a href="#" className="block hover:underline">
                OEM Solution
              </a>
              <a href="#" className="block hover:underline">
                Partner Program
              </a>
            </div>

            <div>
              <ListHeader>Resources</ListHeader>
              <a href="#" className="block hover:underline">
                Blog
              </a>
              <a href="#" className="block hover:underline">
                Events
              </a>
              <a href="#" className="block hover:underline">
                Dell Learning Centre
              </a>
              <a href="#" className="block hover:underline">
                Glossary
              </a>
              <a href="#" className="block hover:underline">
                Privacy Centre
              </a>
              <a href="#" className="block hover:underline">
                Resources Library
              </a>
              <a href="#" className="block hover:underline">
                Trail Software Downloads
              </a>
            </div>
          </div>
        </div>

        {/* Footer Bottom Links */}
        <div className="max-w-screen-2xl mx-auto py-4 flex flex-col md:flex-row justify-between text-center border-t">
          <div className="flex justify-center md:justify-start space-x-4 mb-4 md:mb-0">
            <a href="#" className="hover:underline font-bold">
              Dellco.com
            </a>
            <a href="#" className="hover:underline font-bold">
              Dellco Technologies
            </a>
            <a href="#" className="hover:underline font-bold">
              Premier
            </a>
          </div>
          <div className="flex justify-center md:justify-end space-x-4">
            <a href="#" className="hover:underline">
              © 2025 Dell Inc.
            </a>
            <a href="#" className="hover:underline">
              Terms of Sale
            </a>
            <a href="#" className="hover:underline">
              Privacy Statement
            </a>
            <a href="#" className="hover:underline">
              Legal & Regulatory
            </a>
            <a href="#" className="hover:underline">
              Accessibility
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default FooterPart;
