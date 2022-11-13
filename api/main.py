from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils import ReactionWrapper



app = FastAPI(title="Wrapper for the rdChemReactions.ReactionFromSmarts")


class ReactionHandler(BaseModel):
    reaction_smarts: str
    reactants: str


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.get("/")
def home():
    """Reaction_wrapper. Link to API docs"""
    return "For documentation head over to http://localhost:80/docs"


@app.post("/run_reaction/")
async def get_products_of_reaction(data: ReactionHandler, limits: int = 1000):
    """For a given reaction SMARTS and reactant SMILES check the validity of the input
    and return a list of unique SMILES products
    """
    reaction_smarts = data.reaction_smarts
    reactants = data.reactants
    reaction = ReactionWrapper(reaction_smarts, reactants, limits)
    products = reaction.run_reaction()
    return {"Products": products}
