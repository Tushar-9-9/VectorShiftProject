from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from collections import defaultdict, deque

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust as necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your existing model and endpoint code
class Node(BaseModel):
    id: str
    type: str
    position: Dict[str, float]
    data: Dict[str, str]

class Edge(BaseModel):
    id: str
    source: str
    target: str

class PipelineData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

def is_dag(nodes: List[Node], edges: List[Edge]) -> bool:
    adj_list = defaultdict(list)
    in_degree = defaultdict(int)

    for edge in edges:
        adj_list[edge.source].append(edge.target)
        in_degree[edge.target] += 1

    queue = deque(node.id for node in nodes if in_degree[node.id] == 0)
    visited_count = 0

    while queue:
        node = queue.popleft()
        visited_count += 1
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return visited_count == len(nodes)

@app.post('/pipelines/parse')
async def parse_pipeline(pipeline: PipelineData):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)
    dag_status = is_dag(pipeline.nodes, pipeline.edges)

    return {"num_nodes": num_nodes, "num_edges": num_edges, "is_dag": dag_status}
