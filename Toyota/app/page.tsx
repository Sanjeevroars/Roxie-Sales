import type { HomeProps } from "@/types";
import { Hero } from "@/components";
import { ProductSection } from "@/components";

export default async function Home({ searchParams }: HomeProps) {
  return (
    <main className="overflow-hidden">
      <Hero />
      <ProductSection />
    </main>
  );
}
