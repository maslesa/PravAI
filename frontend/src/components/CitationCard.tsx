import type { Citation } from "../types/api";

interface CitationCardProps {
  citation: Citation;
}

export function CitationCard({
  citation,
}: CitationCardProps) {
  return (
    <div className="rounded-xl border-2 border-mytxt bg-mybg p-4">
      <div className="flex items-start gap-3">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-mytxt/10 text-sm font-semibold text-mytxt">
          <img className="h-5 w-5" src="/doc.png" alt="Icon" />
        </div>

        <div>
          <p className="text-sm font-medium text-mytxt">
            {citation.law}
          </p>

          <p className="mt-1 text-sm text-mytxt/50 italic">
            Član {citation.article}
          </p>
        </div>
      </div>
    </div>
  );
}