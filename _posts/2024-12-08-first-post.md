---
layout: default
title: "A basic application"
slug: a-basic-application
date: 2024-12-08
render_with_liquid: false
---
# A Basic Application

In this post, I describe the basic scaffolding that all my future work will build on top of. I built a simple question and answer application that uses a library of PDFs as a knowledge source. Along the way, I tried to make as few decisions as possible, relying on defaults or recommended settings in tutorials. It works pretty well! but we can do better.

![Screenshot](/rag-playground/assets/screenshot-what-is-a-rag.png)

## Follow along at home

Since this is the scaffolding that all future work will build on, it lives in the [main branch](https://github.com/erikwiffin/rag-playground) of this project.

## The non-RAG basics

Since I decided to build this into a web application, there are a number of non-RAG basics that I needed to get out of the way first. I went with the tools that I know and can get up and running quickly and productively with.

* Backend - flask, python
* Frontend - React, vite, tailwind
* Database - postgres

This is not intended to be a deep exploration of these tools, but this application follows patterns that I've found to be effective in the past.

## The choices to be made while building a RAG

So what is a RAG, specifically? Retrieval Augmented Generation is a technique for solving a common problem and works through a couple steps.

The main problem that it is trying to solve is the issue that Large Language Models (LLMs) don't know everything. They are only exposed to information that was available in their training data, and even that is limited to a highly compressed and lossy version of that information. This means that if you need your LLM to respond with something that was published _after_ it was trained or with something that is only present in your proprietary dataset, it will fail to answer your question or worse, hallucinate a made up answer.

So how do we solve this problem? We tell the LLM the answer at the same time we ask it a question.

The first step is to store the relevant domain knowledge or your proprietary data in a search engine of some kind. This search engine can be a traditional database (PostgreSQL, MySQL), a lexical search engine (Elasticsearch), or more frequently, a vector database (Pinecone, Chroma, but also some modes of PostgreSQL or Elasticsearch).

Which database you use is a **choice** that I will explore in later writing.

Why load your data into a database first, instead of sending it all to your LLM? LLMs have something called a "context window", basically how much information they can respond to at once. As of this writing at the end of 2024, most commercial LLMs are capping out somewhere around 200,000 tokens (tokens are how LLMs interpret text, they are usually a little shorter than a word, a little longer than a single letter). 200,000 is a lot! but it's probably not enough to hold every single word in every single document you want to search.

So we use a database to retrieve just the documents that are relevant to a single query. In fact, we probably break those documents up into even smaller chunks so we can provide the LLM with only the context it needs.

The size of these chunks is another **choice**. You need to balance ease of searching, giving enough context to answer the question, not giving too much context to confuse the LLM, and even cost (typically you have to pay by the token). I'll dig into this more in later posts.

Once you have your data chunked and stored in a database, you need to _retrieve_ that data (the "R" in RAG) and provide it to your LLM in your prompt.

There are a lot of **choices** to be made while writing that prompt.

Once you've done all that, you need to make sure it works. You can ask a few obvious questions and get half the way there, but the only way to know if you've really solved the problem is to watch how your RAG behaves when real users ask it real questions.

For that, you'll need some kind of _observability_ tool coupled with a way of _evaluating_ it's behavior. These are, you guessed it, more **choices** to be made.

## My basic setup

Like I said at the start, I wanted to set up a basic RAG making the simplest and easiest choices I could at every step of the way.

I decided to use PostgreSQL with the pgvector extension as my _search engine_ of choice. I was already using PostgreSQL as my application database, continueing to work with meant that I had one fewer tool to manage in my stack.

For _chunking_, I decided I would simply break my text into 1024 character blocks - cutting paragraphs, sentences, and even words in half. This is long enough to have some content, but short enough to not be overwhelming. It has some pretty obvious drawbacks though; chopping "My house is" and "blue" into two different chunks could be a problem if the question that we want to ask is "what color is my house?".

Once I had my chunks, I used a python library called [SentenceTransformers](https://sbert.net/) to "vectorize" my text (basically turn a bunch of words into a bunch of numbers that pgvector can do math on). I can now vectorize my user's query and sort the documents in the database by [L2 distance](https://en.wikipedia.org/wiki/Euclidean_distance). Why L2 distance? Because that was the first example in the [pgvector Getting Started documentation](https://github.com/pgvector/pgvector?tab=readme-ov-file#getting-started).

The prompt I used was the following:

```
SYSTEM: You are a helpful AI assistant. Answer the user queries.
USER: The following are a series of documents with important information. Say "understood" if you understand.
---
{{documents}}
ASSISTANT: understood
USER: Answer the following question using only information in the provided documents: {{text}}
```

`{{documents}}` gets replaced with my search results (I chose to limit them to 5 results) and `{{text}}` gets replaced with the user's query.

For observability, I'm using a tool called [Langfuse](https://langfuse.com/). It can track your generation requests, the prompt, parameters, and settings used in that request, and save everything as a dataset for future evaluation attemps.

![Langfuse dashboard](/rag-playground/assets/screenshot-langfuse-dashboard.png)

Conveniently, Langfuse also acts as a "prompt manager". This is not strictly required for building with an LLM, but it's extremely convenient and you'll find yourself wanting one soon enough.

![Langfuse dashboard](/rag-playground/assets/screenshot-langfuse-prompt-manager.png)

As you can see in this screenshot, the model I'm using for my LLM is [mistral-nemo-instruct-2407@4bit](https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407) an open-source model from Mistral AI that I can run locally. It's been [quantized](https://www.infoworld.com/article/2336947/what-is-model-quantization-smaller-faster-llms.html) to 4 bits so it can run faster.

For evaluation, I'm looking at the results in Langfuse and marking them as either a hallucination or not. This is a labor-intensive manual approach that will not scale as I expand the usage of my application and complexity of my experiments.

## Next steps

I've made a lot of choices in building this application, and for a truly state-of-the-art question and answer tool, most of these choices are probably wrong. In future posts, I'll be exploring different techniques to improve my application and benchmarking and measuring my improvements at every step of the way.

Is there something in particular you'd like to see me explore? Hit me up at [erik.wiffin@gmail.com](mailto:erik.wiffin@gmail.com); I'd love to hear from you!