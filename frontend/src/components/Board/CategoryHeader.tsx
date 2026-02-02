"use client";
import React from "react";

export default function CategoryHeader({
  name,
  count,
  collapsed,
  onToggle,
  onAdd,
}: {
  name: string;
  count: number;
  collapsed: boolean;
  onToggle: () => void;
  onAdd: () => void;
}) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-3">
        <button
          aria-expanded={!collapsed}
          onClick={onToggle}
          className="p-1 rounded hover:bg-gray-100"
          title={collapsed ? "Expand tasks" : "Collapse tasks"}
        >
          <svg
            className={`w-4 h-4 transform ${collapsed ? "" : "rotate-90"}`}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M8 5l8 7-8 7"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
        <div>
          <h3 className="text-lg font-medium">{name}</h3>
          <div className="text-xs text-[color:var(--muted-text)]">
            {count} tasks
          </div>
        </div>
      </div>
      <div>
        <button className="text-accent text-sm" onClick={onAdd}>
          + Add Task
        </button>
      </div>
    </div>
  );
}
