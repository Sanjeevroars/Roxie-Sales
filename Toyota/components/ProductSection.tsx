import Image from "next/image";

const ProductSection = () => {
  return (
    <div className="products-section mt-20 px-4 py-10">
      <h2 className="text-center text-3xl font-bold mb-8">Our Products</h2>
      <div className="flex justify-center flex-wrap gap-8 mt-20">
        {/* Sedan */}
        <div className="product-item text-center bg-[#dededf] p-8 rounded-3xl">
          <div className="product-image-container mb-4">
            <div className="relative w-60 h-60 mx-auto ">
              <Image
                src="/sedan.jpeg"
                alt="Sedan"
                layout="fill"
                className="object-contain rounded-lg"
              />
            </div>
          </div>
          <h3 className="text-xl font-semibold">Sedans</h3>
        </div>

        {/* SUV */}
        <div className="product-item text-center bg-[#dededf] p-8 rounded-3xl">
          <div className="product-image-container mb-4">
            <div className="relative w-60 h-60 mx-auto">
              <Image
                src="/suv.jpeg"
                alt="SUV"
                layout="fill"
                className="object-contain"
              />
            </div>
          </div>
          <h3 className="text-xl font-semibold">SUVs</h3>
        </div>

        {/* HatchBack */}
        <div className="product-item text-center bg-[#dededf] p-8 rounded-3xl">
          <div className="product-image-container mb-4">
            <div className="relative w-60 h-60 mx-auto">
              <Image
                src="/hatch.jpeg"
                alt="Hatchback"
                layout="fill"
                className="object-contain"
              />
            </div>
          </div>
          <h3 className="text-xl font-semibold">Hatchbacks</h3>
        </div>

        {/* Luxury */}
        <div className="product-item text-center bg-[#dededf] p-8 rounded-3xl">
          <div className="product-image-container mb-4">
            <div className="relative w-60 h-60 mx-auto">
              <Image
                src="/luxury.jpeg"
                alt="Luxury"
                layout="fill"
                className="object-contain"
              />
            </div>
          </div>
          <h3 className="text-xl font-semibold">Luxury Cars</h3>
        </div>
      </div>
    </div>
  );
};

export default ProductSection;
