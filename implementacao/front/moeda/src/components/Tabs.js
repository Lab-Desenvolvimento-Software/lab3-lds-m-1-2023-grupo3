// import React, { useState } from 'react';

// interface Tab {
//   title: string;
//   content: JSX.Element;
// }

// interface TabsProps {
//   tabs: Tab[];
// }

// function Tabs({ tabs }: TabsProps) {
//   const [activeTab, setActiveTab] = useState(0);

//   const handleTabClick = (index: number) => {
//     setActiveTab(index);
//   };

import React, { useState } from 'react';

function Tabs({ tabs }) {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabClick = (index) => {
    setActiveTab(index);
  };


  return (
    <div className="tabs">
      <ul className="tab-list">
        {tabs.map((tab, index) => (
          <li
            key={index}
            className={index === activeTab ? 'active' : ''}
            onClick={() => handleTabClick(index)}
          >
            {tab.title}
          </li>
        ))}
      </ul>
      <div className="tab-content">
        {tabs[activeTab].content}
      </div>
    </div>
  );
}

export default Tabs;

