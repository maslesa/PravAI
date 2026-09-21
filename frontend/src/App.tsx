import { useState } from "react";

import { AnswerCard } from "./components/AnswerCard";
import { QueryInput } from "./components/QueryInput";
import { streamQuestion } from "./services/api";
import type { Citation } from "./types/api";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [citations, setCitations] = useState<Citation[]>([]);
  const [grounded, setGrounded] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!question.trim() || loading) {
      return;
    }

    setLoading(true);
    setError(null);

    setAnswer("");
    setCitations([]);
    setGrounded(false);

    try {
      await streamQuestion(
        question.trim(),
        {
          onToken: (content) => {
            setAnswer(
              (currentAnswer) =>
                currentAnswer + content,
            );
          },

          onMetadata: (
            nextCitations,
            nextGrounded,
          ) => {
            setCitations(nextCitations);
            setGrounded(nextGrounded);
          },
        },
      );
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
    <div className="min-h-screen bg-mybg">
      <header className="border-b border-mybg bg-mybg">
        <div className="mx-auto flex max-w-5xl items-center justify-center px-6 py-4">
          <div className="flex flex-col items-center">
            <h1 className="text-xl font-bold tracking-tight text-mytxt">
              PravAI
            </h1>

            <p className="text-xs text-mytxt/50">
              Legal Research Assistant
            </p>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-6 py-16">
        <div className="text-center">
          <h2 className="text-4xl font-bold tracking-tight text-mytxt sm:text-5xl">
            Istražite zakone
            <br />

            <span className="text-mytxt-light/70">
              uz pomoć PravAI
            </span>
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-base text-mytxt">
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

        {loading && !answer && (
          <div className="mt-8 rounded-2xl border-2 border-mytxt bg-mybg px-6 py-8 text-center shadow-sm">
            <div className="mx-auto mb-4 h-6 w-6 animate-spin rounded-full border-2 border-mytxt/20 border-t-mytxt" />

            <p className="text-sm font-medium text-mytxt">
              PravAI istražuje relevantne odredbe...
            </p>

            <p className="mt-1 text-xs text-mytxt/50">
              Semantic + BM25 retrieval → reranking → Qwen3
            </p>
          </div>
        )}

        {answer && (
          <AnswerCard
            answer={answer}
            citations={citations}
            grounded={grounded}
          />
        )}

        {error && (
          <div className="mt-8 rounded-2xl border-2 border-red-300 bg-red-50 px-5 py-4">
            <p className="text-sm font-medium text-red-800">
              Greška
            </p>

            <p className="mt-1 text-sm text-red-700">
              {error}
            </p>
          </div>
        )}

        <div className="mt-16 border-t-2 border-mytxt pt-6 text-center">
          <p className="text-xs leading-5 text-mytxt/50">
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