import React from 'react';
import { LuX } from "react-icons/lu";

const tags = ['Tagggggggggg', 'Tag', 'Tag', 'Tag', 'Tag', 'Tag', 'Tag', 'Tag','Tag', 'Tag', 'Tag', 'Tag'];

const TagInput = ({ title, icon }) => (
  <div className="bg-white rounded-2xl shadow-md p-4 mb-6">
    <div className="flex items-center gap-2 mb-3">
      {icon}
      <h2 className="font-semibold text-lg">{title}</h2>
    </div>
    <div className="flex flex-col gap-2">
        <div className='flex flex-wrap gap-1'>
        {tags.map((tag, idx) => (
            <div key={idx} className="flex bg-black text-white px-2 py-1 text-xs rounded-lg">
            <span>{tag}</span>
            <button onClick={()=>{console.log("delete")}} className='ml-1'><LuX></LuX></button>
            </div>
        ))}
        </div>
    <div className='flex justify-end'>
    <input
        type="text"
        placeholder="Value"
        className="border rounded-full px-4 py-1 text-sm outline-none"
      />
    </div>
    </div>
  </div>
);

const preferencesView = () => {
  return (
    <>

        {/* Main Content */}
        
          <TagInput
            title="What I like?"
            icon={<span className="text-xl">💜</span>}
          />
          <TagInput
            title="What I dislike?"
            icon={<span className="text-xl">❌</span>}
          />
          <TagInput
            title="Allergies"
            icon={<span className="text-xl">❗</span>}
          />
        
     </>
  );
};


export default preferencesView