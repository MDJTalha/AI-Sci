import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'NeuroScholar - Autonomous Research Agent',
  description: 'AI-powered autonomous research assistant for science and technology',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
