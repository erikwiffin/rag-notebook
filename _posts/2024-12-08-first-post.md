---
layout: default
title: "A basic RAG"
slug: a-basic-rag
date: 2024-12-08
---
# A Basic RAG

In this post, I describe the basic scaffolding that all my future work will build on top of. I built a simple question and answer application that uses a library of PDFs as a knowledge source. Along the way, I tried to make as few decisions as possible, relying on defaults or recommended settings in tutorials. It works pretty well! but we can do better.

![Screenshot](/rag-playground/assets/Screenshot_2024-12-08_at_10.49.20_AM.png)

## Follow along at home

Since this is the scaffolding that all future work will build on, it lives in the [main branch](https://github.com/erikwiffin/rag-playground) of this project.

## The non-RAG basics

Since I decided to build this into a web application, there are a number of non-RAG basics that I needed to get out of the way first. I went with the tools that I know and can get up and running quickly and productively with.

* Backend - flask, python
* Frontend - React, vite, tailwind
* Database - postgres

This is not intended to be a deep exploration of these tools, but this application follows patterns that I've found to be effective in the past.

## To be continued...