# DSA 40 Application Helper

## Development

### Requirements

- `uv`
- `npm`

### Local Setup

#### Backend

in `backend` run `uv run fastapi dev` (make sure port 8000 is not in use)

You can interact with the backend either via the frontend (as far as functionality is implemented) or via the swagger API at `http://localhost:8000/docs`

#### Frontend

in `frontend` run `npm run dev` (make sure port 5173 is not in use)
Browse to `http://localhost:5173` to use the DSA40 Application Helper

#### API

the source of truth for the API definition is the backend.
In case you modify the fastapi backend, make sure to regenerate the API definitions by running `sh scripts/generate_client.sh`

### Troubleshooting

**Missmatched node version when running frontend**

Make sure you are using node >20.
