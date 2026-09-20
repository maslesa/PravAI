import type { Citation } from "../types/api";

interface CitationCardProps {
  citation: Citation;
}

export function CitationCard({
  citation,
}: CitationCardProps) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white p-4">
      <div className="flex items-start gap-3">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-zinc-100 text-sm font-semibold text-zinc-700">
          §
        </div>

        <div>
          <p className="text-sm font-medium text-zinc-900">
            {citation.law}
          </p>

          <p className="mt-1 text-sm text-zinc-500">
            Član {citation.article}
          </p>
        </div>
      </div>
    </div>
  );
}