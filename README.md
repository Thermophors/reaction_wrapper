# Intro

[`ReactionWrapper`](./api/utils.py) is a class for transforming provided reactant SMILES using reaction SMARTS.
This is a "wrapper" for the rdkit's `rdChemRections.RunReactants` method (https://www.rdkit.org/docs/source/rdkit.Chem.rdChemReactions.html). Class constructor contains checks for the validity of the input including the correctness of the SMARTS and SMILES and the compatibility of the reaction and reactants.

The `run_reaction` method is responsible for the generation of products.

Microservice for running the reaction was created using fastAPI and served as a Docker container.


# Install & serve

Build docker image:

```bash
cd api
docker build -t reaction_wrapper .
```

Serve in a local environment (by default the fastAPI is exposed on port `80`).

`docker run --rm -p 80:80  reaction_wrapper`

# Run reactions 

Example usages of a service are in the `demo.ipynb`. `demo.ipnb` uses modules from standard library thus additional virtual env or container is not needed.


## Curl

```bash
curl -X POST http://localhost/run_reaction/?limits=1000 \
  -H "Content-Type: application/json" \
  -d @test.json
```
