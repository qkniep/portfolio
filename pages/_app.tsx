import '../styles/globals.css'
import type { AppProps } from 'next/app'
import PlausibleProvider from 'next-plausible'
import 'windi.css'
import 'animate.css';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <PlausibleProvider domain="example.com">
      <Component {...pageProps} />
    </PlausibleProvider>
  )
}
