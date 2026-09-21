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
      <div className="rounded-2xl border-2 border-mytxt bg-bg shadow-sm">
        <div className="border-b-2 border-m px-6 py-5">
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-lg font-semibold text-mytxt">
              Odgovor
            </h2>

            <span
              className={`rounded-full px-3 py-1 text-xs font-medium ${
                grounded
                  ? "bg-emerald-50 text-emerald-600"
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
          <p className="whitespace-pre-line text-base leading-7 text-mytxt">
            {answer}
          </p>
        </div>
      </div>

      {citations.length > 0 && (
        <div className="mt-6">
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-mytxt">
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