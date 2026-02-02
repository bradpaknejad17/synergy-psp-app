"use client";
import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import TaskRow from "../Task/TaskRow";

export default function CategoryTasks({
  name,
  sortedTasks,
  collapsed,
  containerId,
  onEdit,
}: {
  name: string;
  sortedTasks: any[];
  collapsed: boolean;
  containerId: string;
  onEdit: (task: any) => void;
}) {
  return (
    <AnimatePresence initial={false}>
      {!collapsed && (
        <motion.div
          id={containerId}
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: "auto", opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          transition={{ type: "tween", duration: 0.18 }}
          className="mt-3 space-y-2 overflow-hidden"
        >
          {/* Column labels row to align with TaskRow grid: title 60%, metrics 20%, status 20% */}
          {sortedTasks.length > 0 && (
            <div className="grid grid-cols-12 items-center gap-4 py-2 px-1 text-xs text-[color:var(--muted-text)]">
              <div className="col-span-7">Task</div>
              <div className="col-span-3 text-right">Metric</div>
              <div className="col-span-2 text-right">Due / Status</div>
            </div>
          )}

          {sortedTasks.map((t) => (
            <TaskRow key={t.id} task={t} onOpenEdit={(task) => onEdit(task)} />
          ))}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
