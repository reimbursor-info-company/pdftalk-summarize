"""Command-line interface: pdftalk-summarize input.pdf -o summary.txt"""

import argparse
import sys
from pathlib import Path

from .textrank import summarize


def _read_input(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        try:
            from pdftalk.extractor import PdfTextExtractionError, extract_text
        except ImportError:
            print(
                "Error: reading PDF files requires the 'pdftalk' package. "
                "Install it with: pip install pdftalk-summarize[pdf]",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            return extract_text(path)
        except PdfTextExtractionError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    return path.read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pdftalk-summarize",
        description="Summarize a text or PDF file using an offline extractive algorithm.",
    )
    parser.add_argument("input", help="Path to the input .txt or .pdf file")
    parser.add_argument("-o", "--output", default=None, help="Path to the output summary (.txt). Prints to stdout if omitted")
    parser.add_argument("--ratio", type=float, default=0.2, help="Fraction of sentences to keep (default: 0.2)")
    parser.add_argument("--max-sentences", type=int, default=None, help="Hard cap on the number of sentences kept")
    parser.add_argument("--language", choices=["auto", "es", "en"], default="auto", help="Stopword language (default: auto)")
    parser.add_argument(
        "--audio", default=None, help="Also convert the summary to audio at this path (requires pdftalk)"
    )
    parser.add_argument("--voice-id", default=None, help="System voice ID to use when --audio is set")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        parser.error(f"File does not exist: {input_path}")

    text = _read_input(input_path)

    try:
        summary = summarize(
            text, ratio=args.ratio, max_sentences=args.max_sentences, language=args.language
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(summary, encoding="utf-8")
        print(f"Summary written to: {output_path}")
    else:
        print(summary)

    if args.audio:
        try:
            from pdftalk.converter import text_to_audio
        except ImportError:
            print(
                "Error: --audio requires the 'pdftalk' package. "
                "Install it with: pip install pdftalk-summarize[pdf]",
                file=sys.stderr,
            )
            sys.exit(1)
        audio_path = text_to_audio(summary, args.audio, voice_id=args.voice_id)
        print(f"Audio generated at: {audio_path}")


if __name__ == "__main__":
    main()
