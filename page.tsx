"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"

export default function LandingPage() {
  const router = useRouter()

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem("token")

    // If token exists, redirect to home page
    if (token) {
      router.push("/home")
    } else {
      router.push("/login")
    }
  }, [router])

  return (
    <div className="flex items-center justify-center min-h-screen bg-green-50">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-green-800">Loading...</h1>
      </div>
    </div>
  )
}
