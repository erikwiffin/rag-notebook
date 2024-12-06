from pathlib import Path

from ariadne import (
    MutationType,
    QueryType,
    graphql_sync,
    load_schema_from_path,
    make_executable_schema,
)
from ariadne.explorer import ExplorerGraphiQL
from flask import Blueprint, jsonify, request
from openai import OpenAI
from sentence_transformers import SentenceTransformer

from server.application import app
from server.extensions import db
from server.models.document import Chunk, Document

BP = Blueprint("graphql", __name__)

gql_query = QueryType()
gql_mutation = MutationType()


@gql_query.field("search")
def resolve_search(*_, text):

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode([text])
    vectors = embeddings[0]

    query = db.select(Chunk).order_by(Chunk.vectors.l2_distance(vectors)).limit(5)

    chunks = list(db.session.execute(query).scalars())
    client = OpenAI()

    context = """
The following are a series of documents with important information. Say "understood" if you understand.
---
"""
    for chunk in chunks:
        context += f"\n{chunk.text}"

    completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": context},
            {"role": "assistant", "content": "understood"},
            {
                "role": "user",
                "content": f"Answer the following question using only information in the provided documents: {text}",
            },
        ],
        model="mistral-nemo-instruct-2407@4bit",
        temperature=0.3,
        max_tokens=-1,
        stream=False,
    )

    answer = completion.choices[0].message.content

    print(
        {
            "answer": answer,
            "documents": [chunk.to_json() for chunk in chunks],
        }
    )

    return {
        "answer": answer,
        "documents": [chunk.to_json() for chunk in chunks],
    }


type_defs = load_schema_from_path(Path(BP.root_path) / "schema.graphql")
schema = make_executable_schema(type_defs, gql_query, gql_mutation)

# Retrieve HTML for the GraphiQL.
# If explorer implements logic dependant on current request,
# change the html(None) call to the html(request)
# and move this line to the graphql_explorer function.
explorer_html = ExplorerGraphiQL().html(None)


@BP.route("/graphql", methods=["GET"])
def graphql_explorer():
    # On GET request serve the GraphQL explorer.
    # You don't have to provide the explorer if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL explorer app.
    return explorer_html, 200


@BP.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema, data, context_value={"request": request}, debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
