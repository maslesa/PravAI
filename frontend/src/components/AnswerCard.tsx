import type { Citation } from "../types/api";
import { CitationCard } from "./CitationCard";

interface AnswerCardProps {
  answer: string;
  citations: Citation[];
  grounded: boolean;
}

export function AnswerCard({
  answer,
  citations,
  grounded,
}: AnswerCardProps) {
  return (
    <section className="mt-8">
      <div className="rounded-2xl border border-zinc-200 bg-white shadow-sm">
        <div className="border-b border-zinc-100 px-6 py-5">
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-lg font-semibold text-zinc-900">
              Odgovor
            </h2>

            <span
              className={`rounded-full px-3 py-1 text-xs font-medium ${
                grounded
                  ? "bg-emerald-50 text-emerald-700"
                  : "bg-amber-50 text-amber-700"
              }`}
            >
              {grounded
                ? "Grounded"
                : "Nedovoljno podataka"}
            </span>
          </div>
        </div>

        <div className="px-6 py-6">
          <p className="whitespace-pre-line text-base leading-7 text-zinc-700">
            {answer}
          </p>
        </div>
      </div>

      {citations.length > 0 && (
        <div className="mt-6">
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-zinc-500">
            Izvori
          </h3>

          <div className="grid gap-3 sm:grid-cols-2">
            {citations.map((citation, index) => (
              <CitationCard
                key={`${citation.law}-${citation.article}-${index}`}
                citation={citation}
              />
            ))}
          </div>
        </div>
      )}
    </section>
  );
}