#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# chat_loop.py

from retriever import search_similar_chunks, rerank_results
from embedder import embed_text
from ollama_runner import query_llm
from termcolor import colored
from tqdm import tqdm
import time
import threading

def show_spinner(stop_event):
    with tqdm(total=0, bar_format="{desc}", desc="🤖 Generating response from LLM... (press Ctrl+C to cancel)") as pbar:
        while not stop_event.is_set():
            time.sleep(0.1)

def chat_loop():
    print(colored("📚 Ollama Offline RAG Assistant", "green"))
    print(colored("Type your question below. Type 'exit' to quit.\n", "cyan"))

    while True:
        try:
            query = input("> ").strip()
            if query.lower() in ("exit", "quit", "bye"):
                print(colored("👋 Goodbye! Exiting RAG assistant.\n", "cyan"))
                break

            query_embedding = embed_text(query)
            docs, embs, metas = search_similar_chunks(query_embedding)

            if not docs:
                print(colored("🫥 No relevant documents found. Try rephrasing your question.\n", "yellow"))
                continue

            top_results = rerank_results(query_embedding, docs, embs, metas)

            if not top_results:
                print(colored("🫥 No relevant documents found. Try rephrasing your question.\n", "yellow"))
                continue

            doc, meta, score, warn = top_results[0]

            if warn:
                print(colored("⚠️ Warning: The retrieved document may not be a strong match.\n", "red"))

            print(colored(f"📄 Based on page {meta['page']} of {meta['file']}\n", "cyan"))
            print(doc.strip())
            print()

            # Show LLM spinner
            stop_event = threading.Event()
            spinner_thread = threading.Thread(target=show_spinner, args=(stop_event,))
            spinner_thread.start()

            try:
                start_time = time.time()
                response = query_llm(query, doc)
                elapsed = time.time() - start_time
            finally:
                stop_event.set()
                spinner_thread.join()

            print(colored(f"\n✅ Done in {elapsed:.2f} seconds.\n", "green"))
            print(colored(response.strip(), "white"))
            print()

        except KeyboardInterrupt:
            print(colored("\n👋 Interrupted. Exiting RAG assistant.\n", "cyan"))
            break
        except Exception as e:
            print(colored(f"❌ An error occurred: {e}\n", "red"))
