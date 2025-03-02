
import React from "react";

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  if (totalPages <= 1) return null; // Hide pagination if only one page exists

  const getPageNumbers = () => {
    const pages = [];
    if (totalPages <= 5) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      if (currentPage > 3) pages.push(1, "...");

      const start = Math.max(2, currentPage - 1);
      const end = Math.min(totalPages - 1, currentPage + 1);

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      if (currentPage < totalPages - 2) pages.push("...", totalPages);
    }
    return pages;
  };

  return (
    <div className="mt-6 flex justify-between text-gray-500 text-sm">
      {/* Previous Button */}
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className={`hover:text-black ${
          currentPage === 1 ? "opacity-50 cursor-not-allowed" : ""
        }`}
      >
        ← Previous
      </button>

      {/* Page Numbers */}
      <div className="flex space-x-2">
        {getPageNumbers().map((page, index) => (
          <button
            key={index}
            onClick={() => typeof page === "number" && onPageChange(page)}
            className={`px-3 py-1 rounded ${
              page === currentPage
                ? "bg-black text-white"
                : "hover:text-black"
            }`}
            disabled={page === "..."}
          >
            {page}
          </button>
        ))}
      </div>

      {/* Next Button */}
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className={`hover:text-black ${
          currentPage === totalPages ? "opacity-50 cursor-not-allowed" : ""
        }`}
      >
        Next →
      </button>
    </div>
  );
};

export default Pagination;
