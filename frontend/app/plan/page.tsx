"use client"
import React, {useEffect, useState} from "react"

import { Card, CardContent } from "@/components/ui/card"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
  type CarouselApi,
} from "@/components/ui/carousel"
import { Textarea } from "@/components/ui/textarea"
import { HeaderProvider } from "@/context/HeaderContext";
import Header from "@/components/ui/Header"
import { Button } from "@/components/ui/button"



export function PlanCarousel() {
  const [api, setApi] = React.useState<CarouselApi>()
  const [current, setCurrent] = React.useState(0)
  const [count, setCount] = React.useState(0)
  const [images, setImages] = useState<string[]>([]);

    useEffect(() => {
      const fetchImages = async () => {
        const tempImages: string[] = [];
        for (let i=0; ;i++) {
          const imageUrl = `/images/${i}.png`
          try {
            const response = await fetch(imageUrl, { method: 'HEAD'});
            if (response.ok) {
              tempImages.push(imageUrl)
            }
            else {
              break;
            }
          } catch (error) {
            break;
          }
        }
        
        setCount(tempImages.length);
        tempImages.push('static-card');
        setImages(tempImages);
        
      };
      fetchImages();
    }, []);

  useEffect(() => {
    if (!api) {
      return;
    }
    
    setCurrent(api.selectedScrollSnap() + 1);

    api.on("select", () => {
      setCurrent(api.selectedScrollSnap() + 1)
    });
  }, [api]);

  return (
    <div className="mx-auto max-w-xs">
      <Carousel setApi={setApi} className="w-full max-w-xs">
        <CarouselContent>
          {images.map((image, index) => (
            <CarouselItem key={index}>
              <Card>
                <CardContent className="flex aspect-square items-center justify-center p-6">
                  {image === 'static-card' ? (
                    <div>
                      You have completed all steps! <br />
                      Click <a href="/func-select" className="text-black-500 underline">here</a> to return.
                    </div>

                  ) : (
                    <>
                    <img src={image} />
                    <span className="text-4xl font-semibold">{index + 1}</span>
                    </>
                  )}

                </CardContent>
              </Card>
            </CarouselItem>
          ))}
        </CarouselContent>

        <CarouselNext />
      </Carousel>
      <div className="py-2 text-center text-sm text-muted-foreground">
        Step {current} of {count}
      </div>
    </div>
  )
}

export default function Page() {
    return <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
        <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
            <PlanCarousel />
            <div className="grid w-full gap-2">
              <Textarea placeholder="Write your comments here."/>
              <Button>Log Comment</Button>
            </div>

        </main>
    </div>
}