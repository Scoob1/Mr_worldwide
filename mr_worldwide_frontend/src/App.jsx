import { useState } from 'react'
import './App.css'

function App() {
  const [playlist, setPlaylist] = useState([])
  const [isPlaying, setIsPlaying] = useState(false)

  const fetchPlaylist = async () => {
    const res = await fetch('http://localhost:5000/playlist?limit=10')
    const data = await res.json()
    // Filter out any tracks with missing audio
    setPlaylist(data.filter(t => t.preview_url))
  }

  const handlePlay = (e) => {
    const audios = document.querySelectorAll('audio')
    audios.forEach(a => {
      if (a !== e.target) a.pause()
    })
    setIsPlaying(true)
  }

  const handlePause = () => {
    setIsPlaying(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-zinc-900 to-black text-white flex flex-col items-center p-6 space-y-8">
      <h1 className="text-4xl font-bold text-red-500 drop-shadow-lg">
        Mr._Worldwide x Alien Club 👽🕺
      </h1>

      {/* 🎉 Start Party Button */}
      <button
        onClick={fetchPlaylist}
        className="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-8 rounded-xl shadow-lg"
      >
        Start the Party 🎉
      </button>

      {/* 🛸 Dancing Alien + Pitbull Video */}
      {isPlaying && (
        <div className="w-full max-w-2xl aspect-video shadow-2xl rounded-xl overflow-hidden border-4 border-red-500">
          <iframe
            width="100%"
            height="100%"
            src="https://www.youtube.com/embed/FzG4uDgje3M?autoplay=1&mute=1&loop=1&playlist=FzG4uDgje3M"
            title="Pitbull Dancing with Alien"
            frameBorder="0"
            allow="autoplay; encrypted-media"
            allowFullScreen
          ></iframe>
        </div>
      )}

      {/* 🎵 Playlist */}
      <ul className="mt-4 w-full max-w-xl space-y-4">
        {playlist.map((track, i) => (
          <li
            key={i}
            className="bg-white/10 p-4 rounded flex flex-col sm:flex-row sm:justify-between items-center"
          >
            <span className="text-sm font-semibold">{track.name}</span>
            <audio
              controls
              src={track.preview_url}
              onPlay={handlePlay}
              onPause={handlePause}
              className="mt-2 sm:mt-0"
            />
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
