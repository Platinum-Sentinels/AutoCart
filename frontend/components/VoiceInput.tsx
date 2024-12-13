'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Mic, MicOff } from 'lucide-react'

interface VoiceInputProps {
  onTranscript: (transcript: string) => void
}

export default function VoiceInput({ onTranscript }: VoiceInputProps) {
  const [isListening, setIsListening] = useState(false)
  const [recognition, setRecognition] = useState<any>(null)

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition()
        recognition.continuous = true
        recognition.interimResults = true
        recognition.lang = 'en-US'

        recognition.onresult = (event: any) => {
          const current = event.resultIndex
          const transcript = event.results[current][0].transcript
          onTranscript(transcript)
        }

        setRecognition(recognition)
      }
    }
  }, [onTranscript])

  const toggleListening = () => {
    if (isListening) {
      recognition?.stop()
    } else {
      recognition?.start()
    }
    setIsListening(!isListening)
  }

  return (
    <Button type="button" onClick={toggleListening} variant={isListening ? "destructive" : "outline"} size="icon">
      {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
    </Button>
  )
}

