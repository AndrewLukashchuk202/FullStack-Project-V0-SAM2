'use client'

import { useState, useRef, useEffect } from 'react'
import Image from 'next/image'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"

export default function ImageTagger() {
  const [originalImage, setOriginalImage] = useState<string | null>(null)
  const [processedImage, setProcessedImage] = useState<string | null>(null)
  const [tags, setTags] = useState<{ x: number; y: number; type: 'included' | 'excluded' }[]>([])
  const [images, setImages] = useState<{ id: number; url: string }[]>([])
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (originalImage && canvasRef.current) {
      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')
      const img = new window.Image()
      img.onload = () => {
        canvas.width = img.width
        canvas.height = img.height
        ctx?.drawImage(img, 0, 0)
        drawTags()
      }
      img.src = originalImage
    }
  }, [originalImage])

  useEffect(() => {
    drawTags()
  }, [tags])

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => setOriginalImage(e.target?.result as string)
      reader.readAsDataURL(file)
    }
  }

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!canvasRef.current) return
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    const scaleX = canvas.width / rect.width
    const scaleY = canvas.height / rect.height
    const x = (e.clientX - rect.left) * scaleX
    const y = (e.clientY - rect.top) * scaleY
    const clickCount = e.detail

    if (clickCount === 1) {
      setTags(prevTags => [...prevTags, { x, y, type: 'included' }])
    } else if (clickCount === 2) {
      setTags(prevTags => [...prevTags, { x, y, type: 'excluded' }])
    }
  }

  const drawTags = () => {
    if (!canvasRef.current) return
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Redraw the original image
    if (originalImage) {
      const img = new window.Image()
      img.onload = () => {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
        
        // Draw the tags
        tags.forEach(tag => {
          ctx.beginPath()
          ctx.arc(tag.x, tag.y, 10, 0, 2 * Math.PI)
          ctx.fillStyle = tag.type === 'included' ? 'green' : 'red'
          ctx.fill()
        })
      }
      img.src = originalImage
    }
  }

  const processImage = async () => {
    if (!originalImage) return
    try {
      const formData = new FormData()
      const blob = await fetch(originalImage).then(r => r.blob())
      formData.append('image', blob, 'image.png')
      formData.append('tags', JSON.stringify(tags))

      const response = await fetch('http://127.0.0.1:8000/api/images/', {
        method: 'POST',
        body: formData,
      })
      if (!response.ok) throw new Error('Failed to process image')
        const result = await response.json()
        console.log(result)
        setProcessedImage(result.processed_image)  
    } catch (error) {
      console.error('Error processing image:', error)
    }
  }

  const fetchImages = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/images/')
      if (!response.ok) throw new Error('Failed to fetch images')
      const result = await response.json()
      setImages(result.images)
    } catch (error) {
      console.error('Error fetching images:', error)
    }
  }

  const editImage = (id: number) => {
    const image = images.find(img => img.id === id)
    if (image) setOriginalImage(image.url)
  }

  const deleteImage = async (id: number) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/images/${id}/`, { method: 'DELETE' })
      if (!response.ok) throw new Error('Failed to delete image')
      setImages(images.filter(img => img.id !== id))
    } catch (error) {
      console.error('Error deleting image:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-100 p-8">
      <Card className="max-w-6xl mx-auto bg-white/80 backdrop-blur-sm">
        <CardContent className="p-6">
          <h1 className="text-4xl font-bold text-center mb-8 bg-gradient-to-r from-blue-500 to-purple-500 text-transparent bg-clip-text">
            Image Tagger
          </h1>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div>
              <h2 className="text-2xl mb-4">Original Image</h2>
              <div className="relative">
                <canvas
                  ref={canvasRef}
                  onClick={handleCanvasClick}
                  className="border border-gray-300 w-full"
                  aria-label="Image tagging canvas"
                />
                {!originalImage && (
                  <div className="absolute inset-0 flex items-center justify-center text-gray-400">
                    No image uploaded
                  </div>
                )}
              </div>
              <Input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="mt-4"
                aria-label="Upload image"
              />
            </div>
            <div>
              <h2 className="text-2xl mb-4">Processed Image</h2>
              {processedImage ? (
                <Image src={processedImage} alt="Processed" width={500} height={300} className="w-full" />
              ) : (
                <div className="border border-gray-300 w-full h-[300px] flex items-center justify-center text-gray-400">
                  No processed image yet
                </div>
              )}
            </div>
          </div>
          <div className="flex justify-center space-x-4 mb-8">
            <Button onClick={processImage} variant="default" disabled={!originalImage}>
              Process Image
            </Button>
            <Button onClick={fetchImages} variant="secondary">
              View Image List
            </Button>
          </div>
          {images.length > 0 && (
            <div>
              <h2 className="text-2xl mb-4">Image List</h2>
              <ul className="space-y-4">
                {images.map(image => (
                  <li key={image.id} className="flex items-center space-x-4">
                    <Image src={image.url} alt={`Image ${image.id}`} width={100} height={100} className="rounded-md" />
                    <Button onClick={() => editImage(image.id)} variant="outline">
                      Edit
                    </Button>
                    <Button onClick={() => deleteImage(image.id)} variant="destructive">
                      Delete
                    </Button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}