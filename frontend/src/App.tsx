import { useState } from "react";

import { AnswerCard } from "./components/AnswerCard";
import { QueryInput } from "./components/QueryInput";
import { askQuestion } from "./services/api";
import type { QueryResponse } from "./types/api";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] =
    useState<QueryResponse | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await askQuestion(
        question.trim(),
      );

      setResult(response);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError(
          "Došlo je do greške prilikom obrade pitanja.",
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-50">
      <header className="border-b border-zinc-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-zinc-900">
              PravAI
            </h1>

            <p className="text-xs text-zinc-500">
              Legal Research Assistant
            </p>
          </div>

          <div className="rounded-full border border-zinc-200 bg-zinc-50 px-3 py-1.5 text-xs font-medium text-zinc-600">
            Republika Srbija
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-6 py-16">
        <div className="text-center">
          <div className="mb-4 inline-flex rounded-full border border-zinc-200 bg-white px-3 py-1.5 text-xs font-medium text-zinc-600 shadow-sm">
            AI-powered legal research
          </div>

          <h2 className="text-4xl font-bold tracking-tight text-zinc-900 sm:text-5xl">
            Istražite zakone
            <br />
            <span className="text-zinc-500">
              uz pomoć PravAI
            </span>
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-zinc-500">
            Postavite pitanje o zakonima Republike Srbije.
            PravAI pronalazi relevantne odredbe i generiše
            odgovor zasnovan na dostupnim izvorima.
          </p>
        </div>

        <div className="mt-10">
          <QueryInput
            question={question}
            loading={loading}
            onQuestionChange={setQuestion}
            onSubmit={handleSubmit}
          />
        </div>

        {loading && (
          <div className="mt-8 rounded-2xl border border-zinc-200 bg-white px-6 py-8 text-center shadow-sm">
            <div className="mx-auto mb-4 h-6 w-6 animate-spin rounded-full border-2 border-zinc-200 border-t-zinc-800" />

            <p className="text-sm font-medium text-zinc-700">
              PravAI istražuje relevantne odredbe...
            </p>

            <p className="mt-1 text-xs text-zinc-400">
              Semantic + BM25 retrieval → reranking → Qwen3
            </p>
          </div>
        )}

        {error && (
          <div className="mt-8 rounded-2xl border border-red-200 bg-red-50 px-5 py-4">
            <p className="text-sm font-medium text-red-800">
              Greška
            </p>

            <p className="mt-1 text-sm text-red-700">
              {error}
            </p>
          </div>
        )}

        {result && (
          <AnswerCard
            answer={result.answer}
            citations={result.citations}
            grounded={result.grounded}
          />
        )}

        <div className="mt-16 border-t border-zinc-200 pt-6 text-center">
          <p className="text-xs leading-5 text-zinc-400">
            PravAI je alat za pravno istraživanje i
            informisanje. Ne predstavlja pravni savet niti
            zamenu za kvalifikovanog pravnika.
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;