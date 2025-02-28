import React from 'react'

const Pagination = () => {
  return (
    <div className="mt-6 flex justify-between text-gray-500 text-sm">
    <button className="hover:text-black">← Previous</button>
    <div className="flex space-x-2">
      <button className="bg-black text-white px-3 py-1 rounded">
        1
      </button>
      <button className="hover:text-black">2</button>
      <button className="hover:text-black">3</button>
      <span>...</span>
      <button className="hover:text-black">67</button>
      <button className="hover:text-black">68</button>
    </div>
    <button className="hover:text-black">Next →</button>
  </div>
  )
}

export default Pagination