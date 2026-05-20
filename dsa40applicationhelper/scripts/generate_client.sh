set -x
set -e

cd backend
uv run python -c "import app.main; import json; print(json.dumps(app.main.app.openapi(), indent=2))" > ../frontend/openapi.json
cd ../frontend
npm run generate
